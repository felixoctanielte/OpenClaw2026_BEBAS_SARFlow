import argparse
import json
import re
from datetime import datetime


def first_match(pattern, text, flags=re.I):
    match = re.search(pattern, text, flags)
    return match.group(1).strip() if match else None


def detect_incident_type(text):
    t = text.lower()
    if any(word in t for word in ["pendaki", "gunung", "pos "]) and any(word in t for word in ["hilang", "belum turun", "tersesat"]):
        return "pendaki_hilang"
    if any(word in t for word in ["nelayan", "perahu", "kapal", "laut", "tenggelam"]):
        return "kecelakaan_air"
    if "banjir" in t:
        return "banjir"
    if any(word in t for word in ["orang hilang", "anak hilang", "lansia hilang"]):
        return "orang_hilang"
    if any(word in t for word in ["kecelakaan", "tabrakan"]):
        return "kecelakaan"
    return "lainnya"


def extract_location(text):
    patterns = [
        r"(?:di|sekitar|lokasi|titik terakhir(?:nya)?(?: sekitar)?|dari)\s+([^.\n,]+(?:Gunung|Pos|Pantai|Sungai|Desa|Kecamatan|Kabupaten|Kota|Pulau|Hutan|Jalur)[^.\n]*)",
        r"(Pos\s*\d+[^.\n,]*)",
        r"(Gunung\s+[A-Za-z0-9 .'-]+)",
    ]
    for pattern in patterns:
        value = first_match(pattern, text)
        if value:
            return value.strip()
    return None


def extract_coordinates(text):
    match = re.search(r"(-?\d{1,2}\.\d+)\s*,\s*(-?\d{1,3}\.\d+)", text)
    if not match:
        return {"lat": None, "lng": None}
    return {"lat": float(match.group(1)), "lng": float(match.group(2))}


def extract_time(text):
    patterns = [
        r"(?:terakhir kontak|kontak terakhir|terakhir terlihat|last seen|jam)\s*(?:jam)?\s*(\d{1,2}[.:]\d{2})",
        r"\b(\d{1,2}[.:]\d{2})\b",
    ]
    for pattern in patterns:
        value = first_match(pattern, text)
        if value:
            return value.replace(".", ":") + " WIB"
    return None


def extract_victim_count(text):
    digit = first_match(r"\b(\d+)\s*(?:orang|korban|pendaki|nelayan|wisatawan)\b", text)
    if digit:
        return int(digit)
    words = {
        "satu": 1,
        "seorang": 1,
        "dua": 2,
        "tiga": 3,
        "empat": 4,
        "lima": 5,
    }
    lower = text.lower()
    for word, number in words.items():
        if re.search(rf"\b{word}\s+(orang|korban|pendaki|nelayan|wisatawan)\b", lower):
            return number
    return None


def extract_contact(text):
    phone = first_match(r"(\+?62\d{8,13}|08\d{8,13})", text)
    return phone


def extract_weather_or_field(text):
    signals = []
    lower = text.lower()
    for word in ["hujan", "cuaca buruk", "kabut", "banjir", "longsor", "arus deras", "gelombang tinggi", "sinyal putus"]:
        if word in lower:
            signals.append(word)
    return ", ".join(signals) if signals else None


def extract_clothing(text):
    match = re.search(r"(?:pakai|memakai|pakaian|jaket|baju)\s+([^.\n]+)", text, re.I)
    return match.group(0).strip() if match else None


def compute_risk(data, text):
    score = 0
    red_flags = []
    lower = text.lower()

    def add(points, label):
        nonlocal score
        score += points
        red_flags.append(label)

    if not data["location_text"] or not data["coordinates"]["lat"]:
        add(2, "lokasi/koordinat belum presisi")
    if not data["last_seen_time"]:
        add(2, "waktu terakhir terlihat/kontak belum jelas")
    if data["victim_count"] and data["victim_count"] > 1:
        add(2, "korban lebih dari satu")
    if any(word in lower for word in ["cedera", "sakit", "luka", "hypothermia", "hipotermia", "tenggelam"]):
        add(3, "indikasi cedera/sakit/bahaya fisik")
    if any(word in lower for word in ["anak", "lansia", "disabilitas"]):
        add(3, "korban rentan")
    if any(word in lower for word in ["hujan", "cuaca buruk", "kabut", "longsor", "banjir", "arus deras", "gelombang tinggi"]):
        add(2, "cuaca/lapangan berisiko")
    if any(word in lower for word in ["logistik tinggal sedikit", "tanpa logistik", "kehabisan logistik", "sinyal putus", "hp mati"]):
        add(2, "logistik/komunikasi terbatas")
    if any(word in lower for word in ["sos", "minta tolong", "darurat"]):
        add(3, "sinyal darurat")
    if data["incident_type"] in ["pendaki_hilang", "kecelakaan_air"] or any(word in lower for word in ["hutan", "gunung", "laut", "sungai"]):
        add(2, "medan/lokasi berisiko")
    if not data["reporter"]["contact"]:
        add(2, "kontak pelapor belum ada")

    if score >= 11:
        priority = "Kritis"
    elif score >= 6:
        priority = "Tinggi"
    elif score >= 3:
        priority = "Sedang"
    else:
        priority = "Rendah"

    return score, priority, red_flags


def build_result(text):
    incident_type = detect_incident_type(text)
    location_text = extract_location(text)
    coordinates = extract_coordinates(text)
    last_seen_time = extract_time(text)
    victim_count = extract_victim_count(text)
    contact = extract_contact(text)
    weather = extract_weather_or_field(text)
    clothing = extract_clothing(text)

    missing = []
    if not location_text:
        missing.append("lokasi terakhir")
    if not coordinates["lat"]:
        missing.append("koordinat/link maps")
    if not last_seen_time:
        missing.append("waktu terakhir terlihat/kontak")
    if victim_count is None:
        missing.append("jumlah korban")
    if not contact:
        missing.append("kontak pelapor aktif")
    if not clothing:
        missing.append("pakaian terakhir korban")

    data = {
        "incident_type": incident_type,
        "location_text": location_text,
        "coordinates": coordinates,
        "report_time": datetime.now().astimezone().isoformat(timespec="seconds"),
        "last_seen_time": last_seen_time,
        "victim_count": victim_count,
        "victims": [
            {
                "name": None,
                "age": None,
                "condition": None,
                "last_clothing": clothing,
                "notes": None,
            }
        ],
        "reporter": {
            "name": None,
            "contact": contact,
            "relation": "pelapor/rombongan" if "teman" in text.lower() or "rombongan" in text.lower() else None,
        },
        "weather_or_field_condition": weather,
        "access_notes": None,
        "missing_fields": missing,
        "red_flags": [],
        "administrative_priority": "Rendah",
        "verification_status": "needs_verification",
        "field_confidence": {
            "incident_type": "inferred" if incident_type else "missing",
            "location_text": "confirmed" if location_text else "missing",
            "last_seen_time": "confirmed" if last_seen_time else "missing",
            "victim_count": "confirmed" if victim_count is not None else "missing",
            "reporter_contact": "confirmed" if contact else "missing",
        },
    }

    score, priority, red_flags = compute_risk(data, text)
    data["risk_score"] = score
    data["administrative_priority"] = priority
    data["red_flags"] = red_flags
    return data


def main():
    parser = argparse.ArgumentParser(description="SARFlow deterministic intake extraction and administrative triage.")
    parser.add_argument("--text", default="", help="Incident report text. If empty, stdin is used.")
    args = parser.parse_args()
    text = args.text.strip()
    if not text:
        text = input().strip()
    print(json.dumps(build_result(text), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
