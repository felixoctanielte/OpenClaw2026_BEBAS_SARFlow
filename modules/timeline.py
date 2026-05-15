import json
from datetime import datetime
from pathlib import Path


def _summary_from_incident(incident: dict, event_type: str) -> str:
    incident_type = incident.get("incident_type") or "kejadian"
    location = incident.get("location_text") or "lokasi belum jelas"
    victim_count = incident.get("victim_count")
    victims = f"{victim_count} korban" if victim_count is not None else "jumlah korban belum jelas"
    if event_type == "case_update":
        return f"Update kasus {incident_type} di {location}, {victims}."
    return f"Laporan awal {incident_type} di {location}, {victims}."


def append_timeline_event(path: str, raw_text: str, incident: dict, event_type: str = "new_report") -> dict:
    event = {
        "time": datetime.now().astimezone().isoformat(timespec="seconds"),
        "time_local": datetime.now().strftime("%H:%M WIB"),
        "source": "chat_pelapor",
        "event_type": event_type,
        "summary": _summary_from_incident(incident, event_type),
        "raw_text": raw_text,
        "conflict_count": len(incident.get("conflicts", [])),
        "verification_status": "belum terverifikasi",
    }
    timeline_path = Path(path)
    timeline_path.parent.mkdir(parents=True, exist_ok=True)
    with timeline_path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(event, ensure_ascii=False) + "\n")
    return event


def load_timeline(path: str) -> list[dict]:
    timeline_path = Path(path)
    if not timeline_path.exists():
        return []
    events = []
    for line in timeline_path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        events.append(json.loads(line))
    return events
