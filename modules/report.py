def build_final_report(incident: dict, timeline: list[dict], context_cards: list[dict] | None = None) -> str:
    victim = incident["victims"][0] if incident.get("victims") else {}
    timeline_lines = [
        f"- [{event['time_local']}] {event['summary']} Status: {event['verification_status']}"
        for event in timeline
    ]
    if not timeline_lines:
        timeline_lines = ["- Belum ada timeline operasi."]

    missing_lines = [f"- {field}" for field in incident.get("missing_fields", [])] or ["- Tidak ada field kritis yang kosong."]
    verified_lines = []
    for field, status in incident.get("field_confidence", {}).items():
        if status == "confirmed":
            verified_lines.append(f"- {field}")
    if not verified_lines:
        verified_lines = ["- Belum ada informasi yang terverifikasi penuh."]
    conflict_lines = [
        f"- {item['field']}: sebelumnya `{item['existing']}`, update masuk `{item['incoming']}`"
        for item in incident.get("conflicts", [])
    ] or ["- Tidak ada konflik data yang tercatat."]
    context_lines = [
        f"- {card['source']} ({card['status']}): {card['summary']}"
        for card in (context_cards or [])
    ] or ["- Tidak ada context eksternal yang digunakan."]

    return "\n".join(
        [
            "DRAFT LAPORAN ADMINISTRATIF SAR",
            "Status dokumen: Draft - perlu verifikasi petugas.",
            "",
            "1. Identitas Insiden",
            f"Jenis: {incident.get('incident_type')}",
            f"Lokasi: {incident.get('location_text') or '-'}",
            f"Koordinat: {incident.get('coordinates')}",
            f"Waktu laporan: {incident.get('report_time')}",
            f"Waktu terakhir terlihat/kontak: {incident.get('last_seen_time') or '-'}",
            f"Jumlah korban: {incident.get('victim_count') or '-'}",
            f"Pakaian terakhir: {victim.get('last_clothing') or '-'}",
            f"Pelapor: {incident.get('reporter', {}).get('name') or '-'} / {incident.get('reporter', {}).get('contact') or '-'}",
            f"Akses: {incident.get('access_notes') or '-'}",
            "",
            "2. Ringkasan Kondisi",
            f"Kondisi korban/lapangan: {victim.get('condition') or incident.get('weather_or_field_condition') or '-'}",
            f"Prioritas administratif: {incident.get('administrative_priority')} (skor {incident.get('risk_score')})",
            "",
            "3. Timeline",
            *timeline_lines,
            "",
            "4. Informasi Terkonfirmasi Dari Laporan Awal",
            *verified_lines,
            "",
            "5. Informasi Yang Masih Perlu Dilengkapi",
            *missing_lines,
            "",
            "6. Konflik Data",
            *conflict_lines,
            "",
            "7. Context Eksternal",
            *context_lines,
            "",
            "8. Catatan",
            "AI tidak mengambil keputusan evakuasi final dan tidak menggantikan komando lapangan.",
        ]
    )
