# 🆕 SARFlow — AI Agent Administratif SAR

SARFlow adalah AI agent administratif untuk membantu Komandan Operasi (KOM) dan petugas piket SAR dalam mengumpulkan, mengkategorisasi, dan menyimpulkan laporan bencana atau kondisi membahayakan manusia — mulai dari chat tidak terstruktur hingga draft laporan siap tindak.

Mulai dari [START_HERE.md](START_HERE.md) untuk urutan kerja yang rapi.

---

# 🧠 Core Pipeline

```text
📩 Chat Mentah
   ↓
📋 Intake & Klasifikasi
   ↓
🔍 Ekstraksi Data Terstruktur
   ↓
📚 RAG — SOP Check
   ↓
⚠️ Risk Briefing + Prioritas Administratif
   ↓
📜 Timeline Log
   ↓
📄 Draft Report
```

### Detail Pipeline

| Tahap | Fungsi |
|---|---|
| Intake & Klasifikasi | Identifikasi jenis insiden, urgensi, lokasi awal |
| Extraction | Ambil data siapa, apa, kapan, di mana, berapa |
| RAG SOP Check | Cek kesesuaian SOP berdasarkan SK KBSN 154 |
| Risk Briefing | Menyusun prioritas administratif & red flags |
| Timeline Log | Menyimpan kronologi operasi secara append-only |
| Draft Report | Membuat draft laporan administratif otomatis |

---

# 🚀 Cara Menjalankan

## Windows PowerShell

```powershell
.\start_agent.ps1
```

## Atau langsung via Python

```powershell
python run_orchestrator.py --reset --text "Mas, ada 2 pendaki belum turun dari Pos 3 Gunung Lawu. Terakhir kontak jam 18.10. Logistik tinggal sedikit, hujan, sinyal putus. Pelapor teman rombongan, nomor 081234567890."
```

---

# ✅ Output yang Dihasilkan

- Ringkasan briefing SARFlow
- Missing fields / data yang belum lengkap
- Prioritas administratif
- Pertanyaan follow-up untuk pelapor
- Timeline event di `data/timeline.jsonl`
- Incident state terbaru di `data/incident_state.json`

---

# 🎮 Command Reference

| Command | Fungsi |
|---|---|
| `briefing` | Generate briefing & analisis laporan |
| `update` | Update state insiden |
| `timeline` | Tambahkan event ke timeline |
| `report` | Generate laporan akhir |
| `json` | Output JSON mentah |

## Contoh Penggunaan

```powershell
python run_orchestrator.py --command briefing --text "Longsor di Cikidang, 3 rumah tertimbun"

python run_orchestrator.py --command briefing --include-context --text "Banjir di Garut"

python run_orchestrator.py --command report
```

---

# ⚙️ Flags

| Flag | Fungsi |
|---|---|
| `--reset` | Bersihkan state lama & mulai insiden baru |
| `--include-context` | Tambahkan API context card |

---

# 📂 Struktur Project

```text
SARFlow/
├── run_orchestrator.py
├── start_agent.ps1
├── data/
│   ├── timeline.jsonl
│   ├── incident_state.json
│   └── ...
├── docs/
│   ├── PROJECT_STRUCTURE.md
│   ├── ROADMAP.md
│   ├── API_REQUIREMENTS.md
│   ├── FEATURE_SPEC.md
│   └── DEMO_SCRIPT.md
├── modules/
│   ├── intake.py
│   ├── extraction.py
│   ├── rag_sop.py
│   ├── risk_briefing.py
│   ├── timeline.py
│   └── report.py
├── skills/
└── requirements.txt
```

---

# 🧩 Modules

| Module | Fungsi |
|---|---|
| `intake.py` | Intake & klasifikasi laporan |
| `extraction.py` | Ekstraksi data terstruktur |
| `rag_sop.py` | SOP checker berbasis RAG |
| `risk_briefing.py` | Risk briefing generator |
| `timeline.py` | Timeline manager |
| `report.py` | Draft report generator |

---

# 🤖 AI Agents

## 1. Intake Agent
Menerima laporan mentah dan mengubahnya menjadi data awal yang terstruktur.

## 2. Verification Agent
Mendeteksi missing fields, konflik data, dan kebutuhan verifikasi petugas.

## 3. Context Agent
Mengambil konteks eksternal seperti cuaca, gempa, gunung api, dan kondisi wilayah.

## 4. Risk Briefing Agent
Menyusun prioritas administratif dan red flags berdasarkan SOP.

## 5. Timeline Agent
Mencatat seluruh update operasi secara kronologis.

## 6. Report Generator Agent
Membuat draft laporan PDF/DOCX otomatis.

## 7. Safety Guardrail Agent
Menjaga agar AI tidak melampaui batas kewenangan operasional SAR.

---

# 🔗 Integrasi API Eksternal

SARFlow dapat memanggil API Context Provider (`api_context_sar`) untuk mengambil data kontekstual eksternal.

| API | Fungsi | Status |
|---|---|---|
| Open-Meteo | Cuaca real-time & prakiraan | ✅ Stabil |
| BMKG | Cuaca & peringatan dini | ⚠️ Scrape |
| PetaBencana | Laporan crowdsource | ⚠️ Terbatas |
| Wikipedia | Informasi geografis | ✅ Stabil |
| MAGMA ESDM | Status gunung api | ✅ Stabil |
| BNPB CKAN | Data kebencanaan nasional | ❌ 403 |

---

# 🛡️ Safety Guardrails

| Aturan | Deskripsi |
|---|---|
| 🚫 No final decision | AI tidak mengambil keputusan evakuasi final |
| 🚫 No replace command | Tidak menggantikan komando lapangan |
| 🚫 No unverified spread | Tidak menyebarkan info belum diverifikasi |
| ✅ Human verification | Semua output wajib diverifikasi petugas |
| ✅ Source attribution | Semua data eksternal wajib punya sumber |
| ✅ Missing fields flagged | Data kosong wajib ditandai |

---

# 🔄 Alur Interaksi Lengkap

```text
Pelapor
   ↓
📩 Chat Mentah (WA / Radio / Telegram)
   ↓
📥 KOM / Petugas Piket
   ↓
🧠 SARFlow — Intake & Extraction
   ↓
📡 API Context Provider
   ↓
📚 RAG SOP Check
   ↓
⚠️ Risk Briefing + Timeline
   ↓
📄 Draft Report
   ↓
✅ Verifikasi KOM
   ↓
🚁 Tim SAR Lapangan
```

---

# 📈 Status Pengembangan

| Fitur | Status | Catatan |
|---|---|---|
| Intake & klasifikasi | ✅ Siap | Keyword recognition |
| Structured extraction | ✅ Siap | Missing field detection |
| Timeline logging | ✅ Siap | Append-only jsonl |
| Incident persistence | ✅ Siap | JSON state |
| Risk briefing | ✅ Siap | Priority scoring |
| Draft report | ✅ Siap | Format standar |
| RAG SOP integration | 🔄 Progress | Knowledge expansion |
| API context integration | 🔄 Progress | Multi-API fallback |
| QwenPaw orchestration | 📅 Roadmap | Agent v2 |

---

# 📚 Project Docs

- [docs/PROJECT_STRUCTURE.md](docs/PROJECT_STRUCTURE.md)
- [docs/ROADMAP.md](docs/ROADMAP.md)
- [docs/API_REQUIREMENTS.md](docs/API_REQUIREMENTS.md)
- [docs/FEATURE_SPEC.md](docs/FEATURE_SPEC.md)
- [docs/DEMO_SCRIPT.md](docs/DEMO_SCRIPT.md)

---

# 🐾 QwenPaw

Setup QwenPaw masih dalam tahap persiapan.

File yang sudah disiapkan:

- `qwenpaw_workspace/SARFLOW.md`
- `qwenpaw_skill/sarflow/`
- `sarflow_qwenpaw_skill.zip`

---

# 📌 Filosofi SARFlow

> “Cepat, akurat, selalu mencantumkan sumber.  
> Data adalah amanah.”

SARFlow bukan pengganti petugas SAR.

SARFlow dirancang sebagai AI Co-Pilot administratif untuk membantu petugas bekerja lebih cepat, lebih terstruktur, dan lebih siap dalam kondisi kritis.
