from modules.extraction import extract_incident
from modules.intake import build_follow_up_questions


def test_extract_demo_pendaki_hilang():
    text = (
        "Mas, ada 2 pendaki belum turun dari Pos 3 Gunung Lawu. "
        "Terakhir kontak jam 18.10. Logistik tinggal sedikit, hujan, sinyal putus. "
        "Pelapor teman rombongan, nomor 081234567890."
    )
    incident = extract_incident(text)

    assert incident["incident_type"] == "pendaki_hilang"
    assert incident["victim_count"] == 2
    assert incident["last_seen_time"] == "18:10 WIB"
    assert incident["reporter"]["contact"] == "081234567890"
    assert incident["administrative_priority"] in ["Tinggi", "Kritis"]
    assert "koordinat/link maps" in incident["missing_fields"]


def test_follow_up_prioritizes_missing_critical_fields():
    incident = extract_incident("Ada korban hilang di Gunung X.")
    questions = build_follow_up_questions(incident, max_questions=3)

    assert len(questions) == 3
    assert any("pelapor" in question.lower() for question in questions)


def test_extract_gunung_meletus_mentor_case():
    text = (
        "Ada laporan gunung meletus di sekitar Desa Sumber, 3 warga belum kembali. "
        "Pelapor Budi nomor 081111111111. Korban terakhir terlihat jam 16.30, "
        "salah satu pakai baju biru celana hitam."
    )
    incident = extract_incident(text)

    assert incident["incident_type"] == "gunung_meletus"
    assert incident["location_text"] == "sekitar Desa Sumber"
    assert incident["victim_count"] == 3
    assert incident["reporter"]["name"] == "Budi"
    assert incident["victims"][0]["last_clothing"] == "baju biru, celana hitam"


def test_extract_banjir_case():
    text = (
        "Ada banjir di Desa Melati, 5 warga terjebak di rumah. "
        "Pelapor Andi nomor 081222333444. Air naik sejak jam 20.15, "
        "akses jalan utama tertutup."
    )
    incident = extract_incident(text)

    assert incident["incident_type"] == "banjir"
    assert incident["location_text"] == "Desa Melati"
    assert incident["victim_count"] == 5
    assert incident["reporter"]["name"] == "Andi"
    assert incident["last_seen_time"] == "20:15 WIB"
    assert "terjebak" in incident["victims"][0]["condition"]
    assert "akses jalan utama tertutup" in incident["access_notes"]
    assert incident["administrative_priority"] in ["Tinggi", "Kritis"]


def test_extract_kecelakaan_air_case():
    text = (
        "Laporan perahu nelayan mati mesin di Perairan Tanjung Pasir. "
        "Ada 2 nelayan di kapal, terakhir kontak jam 05.20. "
        "Pelapor Sari nomor 081555666777, gelombang tinggi dan arus deras."
    )
    incident = extract_incident(text)

    assert incident["incident_type"] == "kecelakaan_air"
    assert incident["location_text"] == "Perairan Tanjung Pasir"
    assert incident["victim_count"] == 2
    assert incident["reporter"]["name"] == "Sari"
    assert incident["last_seen_time"] == "05:20 WIB"
    assert "perahu mati mesin" in incident["victims"][0]["condition"]
    assert "gelombang tinggi" in incident["weather_or_field_condition"]
    assert incident["administrative_priority"] in ["Tinggi", "Kritis"]
