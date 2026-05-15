def _value(value, fallback="-"):
    if value is None or value == "" or value == []:
        return fallback
    return value


def build_briefing(incident: dict, follow_up_questions: list[str], sop_context: list[dict] | None = None) -> str:
    victim = incident["victims"][0] if incident.get("victims") else {}
    missing = incident.get("missing_fields") or []
    red_flags = incident.get("red_flags") or []

    lines = [
        "SARFLOW INTAKE",
        "Status: Belum terverifikasi - perlu konfirmasi petugas.",
        "",
        "Ringkasan:",
        f"- Jenis kejadian: {_value(incident.get('incident_type'))}",
        f"- Lokasi: {_value(incident.get('location_text'))}",
        f"- Koordinat: {_value(incident.get('coordinates'))}",
        f"- Waktu terakhir terlihat/kontak: {_value(incident.get('last_seen_time'))}",
        f"- Jumlah korban: {_value(incident.get('victim_count'))}",
        f"- Kondisi korban terakhir: {_value(victim.get('condition'))}",
        f"- Pakaian terakhir: {_value(victim.get('last_clothing'))}",
        f"- Pelapor: {_value(incident.get('reporter', {}).get('name'))} / {_value(incident.get('reporter', {}).get('contact'))}",
        f"- Cuaca/lapangan: {_value(incident.get('weather_or_field_condition'))}",
        f"- Akses: {_value(incident.get('access_notes'))}",
        "",
        f"Prioritas administratif: {incident.get('administrative_priority')} (skor {incident.get('risk_score')})",
        "Alasan red flag:",
    ]

    if red_flags:
        lines.extend([f"- {item}" for item in red_flags])
    else:
        lines.append("- Belum ada red flag kuat dari laporan awal.")

    lines.extend(["", "Data yang masih kurang:"])
    if missing:
        lines.extend([f"- {item}" for item in missing])
    else:
        lines.append("- Tidak ada field kritis yang kosong dari laporan awal.")

    lines.extend(["", "Pertanyaan follow-up:"])
    if follow_up_questions:
        lines.extend([f"{idx}. {question}" for idx, question in enumerate(follow_up_questions, start=1)])
    else:
        lines.append("- Tidak perlu pertanyaan lanjutan kritis saat ini; lanjutkan verifikasi petugas.")

    lines.extend(
        [
            "",
            "Catatan keselamatan:",
            "- Output ini rekomendasi administratif, bukan keputusan evakuasi final.",
            "- Informasi publik/keluarga hanya boleh memakai data yang sudah diverifikasi petugas.",
        ]
    )

    if sop_context:
        source_ids = ", ".join(source["id"] for source in sop_context)
        lines.extend(["", f"RAG/SOP context: {source_ids}"])

    return "\n".join(lines)
