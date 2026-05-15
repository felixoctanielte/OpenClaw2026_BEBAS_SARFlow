# SARFlow Agent

SARFlow adalah AI agent administratif untuk membantu KOM/petugas piket SAR mengumpulkan, mengkategorisasi, dan menyimpulkan laporan bencana atau kondisi membahayakan manusia dari chat tidak terstruktur.

## Core Flow

```text
Chat laporan
-> Intake
-> Extraction
-> RAG SOP check
-> Risk briefing
-> Timeline log
-> Draft report
```

## Run Locally

Windows PowerShell:

```powershell
.\start_agent.ps1
```

Atau langsung:

```powershell
python run_orchestrator.py --reset --text "Mas, ada 2 pendaki belum turun dari Pos 3 Gunung Lawu. Terakhir kontak jam 18.10. Logistik tinggal sedikit, hujan, sinyal putus. Pelapor teman rombongan, nomor 081234567890."
```

Output yang diharapkan:
- briefing SARFlow;
- missing fields;
- prioritas administratif;
- pertanyaan follow-up;
- timeline event di `data/timeline.jsonl`;
- state terakhir di `data/incident_state.json`.

## Commands

```powershell
python run_orchestrator.py --command briefing --text "..."
python run_orchestrator.py --command timeline --text "..."
python run_orchestrator.py --command report --text "..."
python run_orchestrator.py --command json --text "..."
```

Tambahkan `--reset` kalau ingin memulai insiden demo baru agar timeline lama dibersihkan.

## QwenPaw Setup

1. Upload/import `sarflow_qwenpaw_skill.zip` ke QwenPaw `Workspace -> Skills`.
2. Enable skill `sarflow`.
3. Tambahkan persona `KOM - SARFlow` di `Workspace -> Files`.
4. Pastikan Discord channel aktif di `Control -> Channels`.
5. Test di Discord dengan:

```text
SARFLOW INTAKE:
Mas, ada 2 pendaki belum turun dari Pos 3 Gunung Lawu. Terakhir kontak jam 18.10.
Logistik tinggal sedikit, hujan, sinyal putus. Pelapor teman rombongan, nomor 081234567890.
```

## Safety

AI tidak mengambil keputusan evakuasi final, tidak menggantikan komando lapangan, dan tidak menyebarkan informasi belum terverifikasi. Semua output harus diverifikasi petugas.
