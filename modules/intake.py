QUESTION_MAP = {
    "nama pelapor": "Nama pelapor siapa, dan hubungan dengan korban apa?",
    "kontak pelapor aktif": "Nomor/kanal kontak aktif yang bisa dihubungi petugas apa?",
    "lokasi kejadian/lokasi terakhir": "Lokasi terakhir yang diketahui di mana? Jika ada, kirim patokan terdekat.",
    "koordinat/link maps": "Bisa kirim koordinat atau link maps titik terakhir?",
    "waktu terakhir korban terlihat/kontak": "Kapan waktu terakhir korban terlihat atau terakhir menghubungi pelapor?",
    "jumlah korban": "Berapa jumlah korban yang dilaporkan?",
    "pakaian terakhir korban, termasuk baju dan celana": "Pakaian terakhir korban apa, termasuk warna baju/jaket dan celana?",
}


def build_follow_up_questions(incident: dict, max_questions: int = 3) -> list[str]:
    questions = []
    for missing_field in incident.get("missing_fields", []):
        question = QUESTION_MAP.get(missing_field)
        if question and question not in questions:
            questions.append(question)
        if len(questions) >= max_questions:
            break
    return questions

