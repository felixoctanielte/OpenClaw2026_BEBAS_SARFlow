import re
from datetime import datetime


def _first_match(pattern: str, text: str, flags: int = re.I):
    match = re.search(pattern, text, flags)
    return match.group(1).strip() if match else None


def detect_incident_type(text: str) -> str:
    lower = text.lower()
    if any(word in lower for word in ["gunung meletus", "erupsi", "lahar", "abu vulkanik"]):
        return "gunung_meletus"
    if "banjir" in lower or any(word in lower for word in ["air naik", "terendam", "genangan"]):
        return "banjir"
    if any(word in lower for word in ["pendaki", "gunung", "pos "]) and any(
        word in lower for word in ["hilang", "belum turun", "tersesat"]
    ):
        return "pendaki_hilang"
    if any(word in lower for word in ["nelayan", "perahu", "kapal", "laut", "tenggelam", "hanyut", "terseret arus", "mati mesin"]):
        return "kecelakaan_air"
    if any(word in lower for word in ["orang hilang", "anak hilang", "lansia hilang"]):
        return "orang_hilang"
    if any(word in lower for word in ["kecelakaan", "tabrakan"]):
        return "kecelakaan"
    return "lainnya"


def extract_coordinates(text: str) -> dict:
    match = re.search(r"(-?\d{1,2}\.\d+)\s*,\s*(-?\d{1,3}\.\d+)", text)
    if not match:
        return {"lat": None, "lng": None}
    return {"lat": float(match.group(1)), "lng": float(match.group(2))}


def extract_location(text: str) -> str | None:
    patterns = [
        r"(?:di|lokasi|titik terakhir(?:nya)?(?: sekitar)?|dari)\s+((?:sekitar\s+)?(?:Gunung|Pos|Pantai|Sungai|Desa|Kecamatan|Kabupaten|Kota|Pulau|Hutan|Jalur|Perairan|Muara|Pelabuhan|Danau|Waduk|Merapi|Lawu|Semeru|Rinjani)[^.\n,]*)",
        r"(?:sekitar)\s+((?:Gunung|Pos|Pantai|Sungai|Desa|Kecamatan|Kabupaten|Kota|Pulau|Hutan|Jalur|Perairan|Muara|Pelabuhan|Danau|Waduk|Merapi|Lawu|Semeru|Rinjani)[^.\n,]*)",
        r"((?:Gunung|Pos|Pantai|Sungai|Desa|Kecamatan|Kabupaten|Kota|Pulau|Hutan|Jalur|Perairan|Muara|Pelabuhan|Danau|Waduk)\s+[^.\n,]+)",
        r"(Pos\s*\d+[^.\n,]*)",
        r"(Gunung\s+[^.\n,]+)",
        r"(Desa\s+[^.\n,]+)",
        r"(Perairan\s+[^.\n,]+)",
        r"(Pantai\s+[^.\n,]+)",
        r"(Sungai\s+[^.\n,]+)",
    ]
    for pattern in patterns:
        value = _first_match(pattern, text)
        if value:
            return value.strip()
    return None


def extract_last_seen_time(text: str) -> str | None:
    patterns = [
        r"(?:terakhir kontak|kontak terakhir|terakhir terlihat|waktu terakhir|last seen)\s*(?:jam)?\s*(\d{1,2}[.:]\d{2})",
        r"\bjam\s*(\d{1,2}[.:]\d{2})\b",
        r"\b(\d{1,2}[.:]\d{2})\b",
    ]
    for pattern in patterns:
        value = _first_match(pattern, text)
        if value:
            return value.replace(".", ":") + " WIB"
    return None


def extract_victim_count(text: str) -> int | None:
    digit = _first_match(r"\b(\d+)\s*(?:orang|korban|pendaki|nelayan|wisatawan|warga)\b", text)
    if digit:
        return int(digit)
    words = {"satu": 1, "seorang": 1, "dua": 2, "tiga": 3, "empat": 4, "lima": 5}
    lower = text.lower()
    for word, number in words.items():
        if re.search(rf"\b{word}\s+(orang|korban|pendaki|nelayan|wisatawan|warga)\b", lower):
            return number
    return None


def extract_contact(text: str) -> str | None:
    return _first_match(r"(\+?62\d{8,13}|08\d{8,13})", text)


def extract_reporter_name(text: str) -> str | None:
    candidate = _first_match(
        r"(?:nama pelapor|pelapor(?: atas nama)?|saya)\s*[:\-]?\s*([A-Za-z .']{3,40}?)(?=\s+(?:nomor|no|kontak|hp|telepon)\b|[.,\n]|$)",
        text,
    )
    if not candidate:
        return None
    relation_words = ["teman", "rombongan", "keluarga", "warga sekitar"]
    if any(word in candidate.lower() for word in relation_words):
        return None
    return candidate.strip()


def extract_relation(text: str) -> str | None:
    lower = text.lower()
    if re.search(r"\b(pelapor|saya).*(teman|rombongan)\b", lower) or "teman rombongan" in lower:
        return "teman/rombongan"
    if re.search(r"\b(pelapor|saya).*(keluarga|ayah|ibu|kakak|adik)\b", lower):
        return "keluarga"
    if re.search(r"\b(pelapor|saya).*(warga|rt|rw|kepala desa|aparat desa)\b", lower):
        return "warga sekitar"
    return None


def extract_weather_or_field(text: str) -> str | None:
    signals = []
    lower = text.lower()
    for word in [
        "hujan",
        "cuaca buruk",
        "kabut",
        "banjir",
        "longsor",
        "arus deras",
        "gelombang tinggi",
        "sinyal putus",
        "air naik",
        "terendam",
        "akses tertutup",
        "jalan tertutup",
        "perahu mati mesin",
        "kapal mati mesin",
        "hanyut",
        "terseret arus",
        "abu vulkanik",
        "erupsi",
        "lahar",
    ]:
        if word in lower:
            signals.append(word)
    return ", ".join(signals) if signals else None


def extract_last_clothing(text: str) -> str | None:
    clothing_bits = []
    specific_patterns = [
        r"(?:baju|kaos|kemeja)\s+(?:warna\s+)?([A-Za-z]+)",
        r"(?:celana)\s+(?:warna\s+)?([A-Za-z]+)",
        r"(?:jaket)\s+(?:warna\s+)?([A-Za-z]+)",
        r"(?:carrier|tas)\s+(?:warna\s+)?([A-Za-z]+)",
    ]
    for pattern in specific_patterns:
        for match in re.finditer(pattern, text, re.I):
            phrase = match.group(0).strip()
            if phrase not in clothing_bits:
                clothing_bits.append(phrase)
    if clothing_bits:
        return ", ".join(clothing_bits)
    for match in re.finditer(r"(?:pakai|memakai)\s+([^.\n]+)", text, re.I):
        phrase = match.group(0).strip()
        if phrase not in clothing_bits:
            clothing_bits.append(phrase)
    return ", ".join(clothing_bits) if clothing_bits else None


def extract_victim_condition(text: str) -> str | None:
    lower = text.lower()
    signals = []
    if "mati mesin" in lower:
        if "perahu" in lower:
            signals.append("perahu mati mesin")
        elif "kapal" in lower:
            signals.append("kapal mati mesin")
        else:
            signals.append("mati mesin")
    for word in [
        "cedera",
        "sakit",
        "luka",
        "lemas",
        "hipotermia",
        "terjebak",
        "terisolir",
        "terseret arus",
        "hanyut",
        "tenggelam",
        "perahu mati mesin",
        "kapal mati mesin",
        "logistik tinggal sedikit",
        "kehabisan logistik",
        "hp mati",
        "sinyal putus",
        "air naik",
    ]:
        if word in lower:
            signals.append(word)
    return ", ".join(dict.fromkeys(signals)) if signals else None


def extract_access_notes(text: str) -> str | None:
    lower = text.lower()
    notes = []
    for phrase in [
        "akses jalan utama tertutup",
        "akses tertutup",
        "jalan utama tertutup",
        "jalan tertutup",
        "jembatan putus",
        "arus deras",
        "gelombang tinggi",
        "sinyal putus",
    ]:
        if phrase in lower and not any(phrase in existing or existing in phrase for existing in notes):
            notes.append(phrase)
    return ", ".join(notes) if notes else None


def compute_risk(incident: dict, text: str) -> tuple[int, str, list[str]]:
    score = 0
    red_flags = []
    lower = text.lower()

    def add(points: int, label: str) -> None:
        nonlocal score
        score += points
        red_flags.append(label)

    if not incident["location_text"] or not incident["coordinates"]["lat"]:
        add(2, "lokasi/koordinat belum presisi")
    if not incident["last_seen_time"]:
        add(2, "waktu terakhir terlihat/kontak belum jelas")
    if incident["victim_count"] and incident["victim_count"] > 1:
        add(2, "korban lebih dari satu")
    if any(word in lower for word in ["cedera", "sakit", "luka", "hipotermia", "tenggelam"]):
        add(3, "indikasi cedera/sakit/bahaya fisik")
    if any(word in lower for word in ["anak", "lansia", "disabilitas"]):
        add(3, "korban rentan")
    if any(word in lower for word in ["hujan", "cuaca buruk", "kabut", "longsor", "banjir", "air naik", "akses tertutup", "jalan tertutup", "arus deras", "gelombang tinggi", "erupsi", "abu vulkanik", "lahar"]):
        add(2, "cuaca/lapangan berisiko")
    if any(word in lower for word in ["logistik tinggal sedikit", "tanpa logistik", "kehabisan logistik", "sinyal putus", "hp mati"]):
        add(2, "logistik/komunikasi terbatas")
    if any(word in lower for word in ["sos", "minta tolong", "darurat"]):
        add(3, "sinyal darurat")
    if any(word in lower for word in ["terjebak", "terisolir", "tenggelam", "hanyut", "terseret arus", "mati mesin"]):
        add(2, "korban dalam kondisi membutuhkan verifikasi cepat")
    if incident["incident_type"] in ["pendaki_hilang", "kecelakaan_air", "gunung_meletus", "banjir"] or any(word in lower for word in ["hutan", "gunung", "laut", "sungai"]):
        add(2, "medan/lokasi berisiko")
    if not incident["reporter"]["contact"]:
        add(2, "kontak pelapor belum ada")
    if any(word in lower for word in ["pelapor hilang", "chat hilang", "tidak bisa dihubungi", "tiba-tiba hilang"]):
        add(2, "kontak lanjutan dengan pelapor/korban terputus")

    if score >= 11:
        priority = "Kritis"
    elif score >= 6:
        priority = "Tinggi"
    elif score >= 3:
        priority = "Sedang"
    else:
        priority = "Rendah"
    return score, priority, red_flags


def extract_incident(text: str) -> dict:
    incident = {
        "incident_type": detect_incident_type(text),
        "location_text": extract_location(text),
        "coordinates": extract_coordinates(text),
        "report_time": datetime.now().astimezone().isoformat(timespec="seconds"),
        "last_seen_time": extract_last_seen_time(text),
        "victim_count": extract_victim_count(text),
        "victims": [
            {
                "name": None,
                "age": None,
                "condition": extract_victim_condition(text),
                "last_clothing": extract_last_clothing(text),
                "notes": None,
            }
        ],
        "reporter": {
            "name": extract_reporter_name(text),
            "contact": extract_contact(text),
            "relation": extract_relation(text),
        },
        "weather_or_field_condition": extract_weather_or_field(text),
        "access_notes": extract_access_notes(text),
        "missing_fields": [],
        "red_flags": [],
        "administrative_priority": "Rendah",
        "verification_status": "needs_verification",
        "field_confidence": {},
    }

    missing = []
    if not incident["reporter"]["name"]:
        missing.append("nama pelapor")
    if not incident["reporter"]["contact"]:
        missing.append("kontak pelapor aktif")
    if not incident["location_text"]:
        missing.append("lokasi kejadian/lokasi terakhir")
    if not incident["coordinates"]["lat"]:
        missing.append("koordinat/link maps")
    if not incident["last_seen_time"]:
        missing.append("waktu terakhir korban terlihat/kontak")
    if incident["victim_count"] is None:
        missing.append("jumlah korban")
    if not incident["victims"][0]["last_clothing"]:
        missing.append("pakaian terakhir korban, termasuk baju dan celana")

    incident["missing_fields"] = missing
    incident["field_confidence"] = {
        "incident_type": "inferred" if incident["incident_type"] != "lainnya" else "missing",
        "location_text": "confirmed" if incident["location_text"] else "missing",
        "coordinates": "confirmed" if incident["coordinates"]["lat"] else "missing",
        "last_seen_time": "confirmed" if incident["last_seen_time"] else "missing",
        "victim_count": "confirmed" if incident["victim_count"] is not None else "missing",
        "reporter_name": "confirmed" if incident["reporter"]["name"] else "missing",
        "reporter_contact": "confirmed" if incident["reporter"]["contact"] else "missing",
        "last_clothing": "confirmed" if incident["victims"][0]["last_clothing"] else "missing",
    }
    score, priority, red_flags = compute_risk(incident, text)
    incident["risk_score"] = score
    incident["administrative_priority"] = priority
    incident["red_flags"] = red_flags
    return incident
