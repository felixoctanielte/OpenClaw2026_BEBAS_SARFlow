# Project Structure

## Root Files

- `START_HERE.md`: dokumen pembuka dan arah kerja.
- `README.md`: cara run cepat dan ringkasan project.
- `PROBLEM_SOLUTION.md`: problem, solution, benefit untuk pitch.
- `agent-config.yml`: konfigurasi runtime agent.
- `RAG_sources.yaml`: daftar sumber knowledge base.
- `run_orchestrator.py`: entry point lokal.
- `requirements.txt`: dependency Python.
- `start_agent.ps1` / `start_agent.sh`: wrapper run lokal.

## Runtime Modules

- `modules/intake.py`: membuat pertanyaan follow-up.
- `modules/extraction.py`: ekstraksi data dari chat.
- `modules/briefing.py`: membuat briefing insiden.
- `modules/timeline.py`: menyimpan timeline event.
- `modules/report.py`: membuat draft laporan.
- `modules/rag.py`: retrieval sederhana dari knowledge base.
- `modules/api_clients.py`: wrapper API eksternal, masih opsional.

## Knowledge Base

- `knowledge_base/sar_sop_sk_kbsn_154.md`: ringkasan SOP dari SK KBSN 154.
- `knowledge_base/rag_design.md`: desain RAG.
- `knowledge_base/api_sources.md`: referensi API eksternal.

## Templates

- `templates/incident_report.md`: template laporan insiden.
- `templates/timeline.md`: template timeline operasi.

## QwenPaw Later

- `qwenpaw_skill/sarflow/`: skill SARFlow untuk QwenPaw.
- `qwenpaw_workspace/SARFLOW.md`: persona yang nanti dipasang di QwenPaw.
- `sarflow_qwenpaw_skill.zip`: zip skill untuk import ke QwenPaw.

Untuk sekarang, jangan fokus ke QwenPaw dulu. Pastikan runtime lokal dan demo story stabil.

## Generated/Runtime Data

- `data/incident_state.json`: state terakhir, generated.
- `data/timeline.jsonl`: timeline runtime, generated.

File generated tidak perlu masuk submission sebagai source utama. `data/.gitkeep` hanya menjaga folder tetap ada.

