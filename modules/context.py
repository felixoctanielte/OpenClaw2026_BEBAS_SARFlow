from modules.api_clients import fetch_bmkg_weather, fetch_petabencana_reports


def build_context_cards(
    cfg: dict,
    incident: dict,
    include_context: bool = False,
    bmkg_adm4: str = "",
    petabencana_admin: str = "",
) -> list[dict]:
    if not include_context:
        return []

    cards = []
    cards.append(_bmkg_weather_card(cfg, bmkg_adm4))
    cards.append(_petabencana_card(cfg, incident, petabencana_admin))
    return cards


def _bmkg_weather_card(cfg: dict, adm4: str) -> dict:
    if not adm4:
        return {
            "source": "BMKG",
            "type": "weather_forecast",
            "status": "skipped",
            "summary": "Kode wilayah adm4 belum tersedia; minta koordinat/lokasi presisi dulu.",
            "trust": "external_context_not_case_fact",
        }

    if not cfg.get("agent", {}).get("api", {}).get("bmkg", {}).get("enabled", False):
        return {
            "source": "BMKG",
            "type": "weather_forecast",
            "status": "disabled",
            "summary": "BMKG context belum diaktifkan di agent-config.yml.",
            "trust": "external_context_not_case_fact",
        }

    try:
        data = fetch_bmkg_weather(adm4)
    except Exception as exc:  # noqa: BLE001 - context cards must fail soft
        return {
            "source": "BMKG",
            "type": "weather_forecast",
            "status": "error",
            "summary": f"BMKG context gagal diambil: {exc}",
            "trust": "external_context_not_case_fact",
        }

    return {
        "source": "BMKG",
        "type": "weather_forecast",
        "status": "ok",
        "summary": "Prakiraan cuaca berhasil diambil. Gunakan sebagai context dan tampilkan atribusi Sumber: BMKG.",
        "trust": "external_context_not_case_fact",
        "raw_preview": _preview(data),
    }


def _petabencana_card(cfg: dict, incident: dict, admin: str) -> dict:
    if not cfg.get("agent", {}).get("api", {}).get("petabencana", {}).get("enabled", False):
        return {
            "source": "PetaBencana",
            "type": "crowdsourced_reports",
            "status": "disabled",
            "summary": "PetaBencana context belum diaktifkan di agent-config.yml.",
            "trust": "external_context_not_case_fact",
        }

    disaster = _map_disaster(incident.get("incident_type"))
    try:
        data = fetch_petabencana_reports(disaster=disaster, admin=admin or None)
    except Exception as exc:  # noqa: BLE001 - context cards must fail soft
        return {
            "source": "PetaBencana",
            "type": "crowdsourced_reports",
            "status": "error",
            "summary": f"PetaBencana context gagal diambil: {exc}",
            "trust": "external_context_not_case_fact",
        }

    return {
        "source": "PetaBencana",
        "type": "crowdsourced_reports",
        "status": "ok",
        "summary": "Laporan publik berhasil diambil. Data urun-daya tidak otomatis memverifikasi kasus SAR.",
        "trust": "external_context_not_case_fact",
        "raw_preview": _preview(data),
    }


def _map_disaster(incident_type: str | None) -> str | None:
    mapping = {
        "banjir": "flood",
        "gunung_meletus": "volcano",
    }
    return mapping.get(incident_type or "")


def _preview(data) -> str:
    text = str(data)
    return text[:500] + ("..." if len(text) > 500 else "")

