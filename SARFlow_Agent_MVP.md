# SARFlow Agent - MVP Plan

## One-line Pitch

SARFlow Agent adalah AI co-pilot untuk petugas piket/KOM yang membantu intake laporan darurat, mengekstrak data insiden, membuat triage administratif dan incident briefing, serta mencatat timeline operasi sampai menjadi draft laporan akhir.

## Positioning

Ide utamanya bukan "AI pencari korban". Posisi yang lebih kuat dan aman:

> AI Agent untuk administrasi awal operasi SAR: intake, verifikasi informasi, briefing insiden, prioritas awal, timeline log, dan draft laporan. Semua output wajib diverifikasi petugas.

Ini cocok dengan OpenClaw Agenthon karena sistem tidak berhenti di chatbot. Agent menjalankan workflow end-to-end: menerima laporan tidak terstruktur, menanyakan data yang kurang, memanggil tool/RAG/API, menyusun briefing, dan membuat timeline/laporan.

## Problem Statement

Saat laporan darurat masuk, informasi sering tidak lengkap: lokasi tidak presisi, waktu terakhir korban terlihat tidak jelas, jumlah korban belum pasti, kondisi korban tidak lengkap, dan kontak pelapor kadang sulit dihubungi. Petugas harus tetap cepat melakukan verifikasi, koordinasi, dan pencatatan timeline. Karena fokus petugas banyak terserap ke operasi lapangan, dokumentasi sering tertunda atau tidak lengkap.

SARFlow membantu pekerjaan administratif yang repetitif dan time-sensitive tanpa mengambil alih keputusan operasional.

## Target User

User utama: petugas piket/KOM yang menerima laporan, melakukan pencatatan awal, dan menyiapkan bahan koordinasi.

User sekunder:
- Koordinator operasi yang butuh ringkasan cepat.
- Admin dokumentasi yang butuh timeline dan draft laporan.
- Tim demo/hackathon yang perlu menunjukkan workflow SAR realistis dengan data dummy.

## Safety Boundaries

SARFlow harus selalu menampilkan batasan berikut:

- AI tidak mengambil keputusan evakuasi final.
- AI tidak menggantikan komando lapangan.
- AI tidak menyebarkan informasi belum terverifikasi.
- AI tidak menyimpulkan lokasi korban secara pasti.
- Semua output adalah rekomendasi administratif untuk diverifikasi petugas.

Output yang mengandung data belum valid harus diberi label:

`Belum terverifikasi - perlu konfirmasi petugas.`

## Four MVP Features

### 1. Chat Intake Laporan

Input berupa chat natural seperti laporan WhatsApp:

```text
Mas, ada 2 pendaki belum turun dari Pos 3 Gunung X. Terakhir kontak jam 18.10.
Katanya logistik tinggal sedikit, hujan, sinyal putus. Pelapor teman rombongan.
```

Agent melakukan:
- Menenangkan dan mengarahkan percakapan.
- Menanyakan data minimum yang belum ada.
- Menghindari pertanyaan terlalu banyak sekaligus.
- Menyimpan setiap jawaban sebagai update insiden.

Pertanyaan follow-up prioritas:
- Lokasi terakhir yang diketahui, titik koordinat/link maps jika ada.
- Waktu terakhir terlihat/terhubung.
- Jumlah korban dan identitas/ciri penting.
- Pakaian terakhir korban.
- Kondisi korban terakhir: cedera, sakit, logistik, alat komunikasi.
- Kontak pelapor aktif dan hubungan dengan korban.
- Akses menuju lokasi dan kondisi cuaca/lapangan.

### 2. Auto-extract Data Insiden

Agent mengubah chat tidak terstruktur menjadi schema:

```json
{
  "incident_type": "pendaki_hilang",
  "location_text": "Pos 3 Gunung X",
  "coordinates": null,
  "last_seen_time": "18:10 WIB",
  "report_time": "2026-05-15T21:30:00+07:00",
  "victim_count": 2,
  "victims": [
    {
      "name": null,
      "age": null,
      "condition": "logistik menipis",
      "last_clothing": null
    }
  ],
  "reporter": {
    "name": null,
    "contact": null,
    "relation": "teman rombongan"
  },
  "weather_or_field_condition": "hujan, sinyal putus",
  "missing_fields": [
    "koordinat/link maps",
    "nama korban",
    "pakaian terakhir",
    "kontak pelapor aktif"
  ],
  "verification_status": "needs_verification"
}
```

Semua field diberi status confidence:
- `confirmed`: disebut jelas oleh pelapor/petugas.
- `inferred`: disimpulkan dari teks, perlu dicek.
- `missing`: belum ada.

### 3. Risk Triage + Incident Briefing

Triage bukan keputusan final. Triage adalah prioritas administratif awal agar petugas tahu mana yang harus diverifikasi dulu.

Sinyal risiko tinggi:
- Anak kecil, lansia, atau korban rentan.
- Cedera/sakit.
- Cuaca ekstrem.
- Korban tanpa logistik.
- Sinyal SOS terakhir.
- Lokasi rawan longsor/banjir/arus.
- Banyak korban.
- Waktu terakhir terlihat sudah lama.
- Kontak korban/pelapor terputus.

Output briefing ideal:

```text
INSIDEN SAR

Jenis: Pendaki hilang
Lokasi: Pos 3 Gunung X
Waktu laporan: 21:30 WIB
Waktu terakhir kontak: 18:10 WIB
Korban: 2 orang
Kondisi terakhir: Logistik menipis, sinyal putus
Cuaca/lapangan: Hujan
Informasi kritis belum ada: Koordinat, pakaian terakhir, kontak aktif pelapor
Red flag: Cuaca hujan, sinyal putus, logistik menipis, korban lebih dari 1
Prioritas administratif: Tinggi
Rekomendasi verifikasi: Minta share live location/titik terakhir, data identitas korban, pakaian terakhir, dan kontak keluarga/rombongan.
Status: Belum terverifikasi - perlu konfirmasi petugas.
```

### 4. Auto-log Timeline + Draft Laporan Akhir

Setiap chat/update masuk otomatis menjadi timeline event:

```json
{
  "time": "2026-05-15T21:35:00+07:00",
  "source": "chat_pelapor",
  "event_type": "new_information",
  "summary": "Pelapor menyebut 2 pendaki terakhir kontak jam 18:10 di sekitar Pos 3.",
  "verification_status": "unverified"
}
```

Event penting:
- Laporan diterima.
- Data pelapor dicatat.
- Lokasi awal diperoleh.
- Permintaan verifikasi dikirim.
- Koordinat diperbarui.
- Tim/instansi terkait dicatat.
- Update cuaca/lapangan.
- Status korban diperbarui.
- Operasi ditutup.

Draft laporan akhir dibuat dari timeline, bukan dari ingatan manual.

## Where RAG Fits

RAG harus dipakai untuk membatasi dan memperkuat workflow, bukan untuk menebak keputusan operasi.

RAG dipakai pada:
- Checklist intake berdasarkan SOP pelayanan SAR.
- Validasi data minimum laporan.
- Penyusunan briefing sesuai format operasi.
- Guardrail komunikasi: mana yang boleh/tidak boleh disampaikan.
- Draft laporan akhir berdasarkan template dan timeline.
- Edukasi singkat "Kenali Basarnas" untuk Gen Z/milenial sebagai mode tambahan, bukan fitur utama.

RAG tidak dipakai untuk:
- Menentukan lokasi korban secara pasti.
- Memutuskan evakuasi.
- Menyebarkan informasi publik tanpa verifikasi.
- Mengganti komando lapangan.

## Agent Architecture

### KOM Orchestrator

KOM adalah agent utama yang mengatur alur:
1. Menerima input chat.
2. Memanggil Extraction Agent.
3. Memanggil RAG untuk SOP/checklist.
4. Memanggil tools eksternal bila relevan.
5. Meminta Risk Briefing Agent membuat rekomendasi administratif.
6. Meminta Timeline Agent mencatat event.
7. Menghasilkan output untuk petugas.

### Intake Agent

Tugas:
- Menjaga percakapan tetap singkat dan jelas.
- Menghasilkan pertanyaan lanjutan berdasarkan missing fields.
- Memprioritaskan data kritis: lokasi, waktu terakhir, korban, kontak.

### Extraction Agent

Tugas:
- Parsing chat menjadi JSON insiden.
- Memberi confidence per field.
- Menandai konflik informasi.

### Risk Briefing Agent

Tugas:
- Menghitung prioritas administratif dengan rule-based scoring.
- Mengambil SOP dari RAG.
- Menyusun briefing singkat.

### Timeline Report Agent

Tugas:
- Mengubah update menjadi timeline.
- Menyusun draft laporan akhir.
- Menjaga status verifikasi setiap event.

## Suggested Tools/API

PetaBencana:
- `/reports`: laporan urun-daya bencana real-time, default last 3 hours, mendukung filter disaster dan admin.
- `/floods`: status area banjir dan tingkat keparahan.
- `/floodgauges`: pemantauan tinggi muka air, saat ini terdokumentasi untuk Jakarta.
- `/stats/reportsSummary`: ringkasan statistik laporan urun-daya.

BMKG:
- Prakiraan cuaca terbuka per desa/kelurahan dengan kode wilayah `adm4`.
- Data 3 hari, per 3 jam, update 2 kali sehari.
- Cocok untuk konteks cuaca di briefing, bukan untuk keputusan operasi final.

BNPB Satu Data:
- Portal dataset dan CKAN API untuk data historis/rujukan kebencanaan.
- Lebih cocok untuk background context dan visualisasi risiko, bukan update real-time SAR.

Satu Peta MKG:
- Layer geospasial BMKG seperti curah hujan, potensi angin, seismisitas, dan FDRS.
- Cocok untuk map layer tambahan bila demo punya peta.

## Recommended 12-hour Build Scope

Build yang paling realistis:
- Chat intake UI.
- Incident dashboard.
- Structured extraction JSON.
- RAG knowledge base dari SOP SK KBSN 154 dan template internal.
- Risk triage rule-based.
- Incident briefing generator.
- Timeline log.
- Draft final report.
- Optional: PetaBencana API card untuk kasus banjir.

Jangan habiskan waktu untuk:
- Prediksi lokasi korban.
- Dispatch/route optimization.
- Integrasi WhatsApp asli.
- Auth kompleks.
- Multi-role permission detail.

## Demo Scenario

Skenario utama: "Pendaki Hilang di Gunung"

Alur demo:
1. Pelapor mengirim chat tidak terstruktur.
2. SARFlow mengekstrak data insiden dan menandai data yang hilang.
3. SARFlow menanyakan 2-3 pertanyaan follow-up paling kritis.
4. Setelah jawaban masuk, SARFlow memperbarui briefing.
5. Agent memberi prioritas administratif "Tinggi" dengan alasan red flag.
6. Timeline otomatis bertambah.
7. Draft laporan akhir dibuat dari timeline.

Why this works:
- Realistis untuk SAR.
- Data bisa dummy.
- Tidak sensitif berlebihan.
- Memperlihatkan agentic workflow, RAG, structured extraction, tool usage, dan audit trail.

## Pitch Deck Outline

1. Problem Statement
2. Solution Overview: SARFlow Agent untuk KOM/petugas piket
3. Agent Workflow and Architecture
4. Key Features
5. RAG and Safety Guardrails
6. Demo Scenario
7. Tech Stack
8. Impact and Future Development

## Devpost Description Draft

SARFlow Agent is an AI co-pilot for search and rescue administrative workflows. Emergency reports often arrive incomplete and unstructured, while officers need to verify location, last-seen time, victim details, reporter contact, and field conditions quickly. SARFlow turns chaotic intake messages into structured incident data, highlights missing critical information, creates a risk-aware incident briefing, and automatically logs the operation timeline for final reporting.

SARFlow does not make evacuation decisions, replace field command, or publish unverified information. All outputs are administrative recommendations that must be verified by authorized officers.

## Future Development

- WhatsApp/Telegram intake connector.
- Voice/radio transcript ingestion.
- Map-based incident board.
- BMKG weather context by location.
- PetaBencana contextual disaster feed.
- Role-based verification workflow.
- Export to PDF report template.
- Offline-first mode for poor connectivity.
