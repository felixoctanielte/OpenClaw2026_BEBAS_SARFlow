from modules.extraction import extract_incident
from modules.context import build_context_cards
from modules.intake import build_follow_up_questions
from modules.rag import load_rag_sources, search_rag
from modules.state import merge_incidents


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


def test_update_merge_adds_coordinates_and_clothing():
    initial = extract_incident(
        "Ada 2 pendaki belum turun dari Pos 3 Gunung Lawu. Terakhir kontak jam 18.10. "
        "Pelapor Rina nomor 081234567890."
    )
    update = extract_incident("Update: koordinat terakhir -7.6275, 111.1942. Korban pakai jaket merah celana hitam.")
    merged = merge_incidents(initial, update, "Update koordinat dan pakaian.")

    assert merged["incident_type"] == "pendaki_hilang"
    assert merged["coordinates"] == {"lat": -7.6275, "lng": 111.1942}
    assert merged["victims"][0]["last_clothing"] == "celana hitam, jaket merah"
    assert "koordinat/link maps" not in merged["missing_fields"]
    assert not merged["conflicts"]


def test_update_marks_conflicting_victim_count():
    initial = extract_incident(
        "Ada 2 pendaki belum turun dari Pos 3 Gunung Lawu. Terakhir kontak jam 18.10. "
        "Pelapor Rina nomor 081234567890."
    )
    update = extract_incident("Update: ternyata ada 3 pendaki di rombongan.")
    merged = merge_incidents(initial, update, "Update jumlah korban.")

    assert merged["victim_count"] == 2
    assert merged["conflicts"]
    assert merged["conflicts"][0]["field"] == "victim_count"


def test_rag_loads_structured_sop_chunks():
    docs = load_rag_sources("RAG_sources.yaml")
    chunk_ids = [doc["id"] for doc in docs]
    results = search_rag(docs, "identitas pelapor kontak verifikasi", limit=5)

    assert any(doc_id.startswith("sar_sop_chunks:") for doc_id in chunk_ids)
    assert any(result["id"].startswith("sar_sop_chunks:") for result in results)


def test_context_cards_are_optional_and_fail_soft():
    incident = extract_incident("Ada banjir di Desa Melati, 5 warga terjebak.")
    cfg = {"agent": {"api": {"bmkg": {"enabled": False}, "petabencana": {"enabled": False}}}}

    assert build_context_cards(cfg, incident, include_context=False) == []

    cards = build_context_cards(cfg, incident, include_context=True)
    assert cards[0]["source"] == "BMKG"
    assert cards[0]["status"] == "skipped"
    assert cards[1]["source"] == "PetaBencana"
    assert cards[1]["status"] == "disabled"
