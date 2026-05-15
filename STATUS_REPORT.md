# SARFlow Status Report

## Current Status

Core local runtime is ready for structured demo and QwenPaw packaging.

Validated scenarios:

- pendaki hilang;
- gunung meletus;
- banjir;
- kecelakaan air;
- multi-turn update;
- conflict detection;
- structured SOP/RAG chunk loading.

Latest validation:

```text
9 tests passing
```

## SOP/RAG Status

Done:

- Manual SOP summary from SK KBSN 154 scanned pages 6-8.
- Structured SOP chunks under `knowledge_base/sop_chunks/`.
- RAG source config in `RAG_sources.yaml`.
- Runtime retriever can load single Markdown files and folder-based chunks.
- Briefing shows source labels, not long noisy excerpts.

Limit:

- Full 41-page OCR has not been completed.
- Current SOP claim should be phrased as "RAG ringan berbasis ringkasan SOP dan chunk terstruktur", not "full SOP OCR".

## Runtime Status

Done:

- intake parsing;
- extraction JSON;
- missing-field detection;
- follow-up questions;
- administrative risk scoring;
- briefing;
- timeline logging;
- report drafting;
- state merge for updates;
- conflict marking;
- optional external context cards.
- `report`, `briefing`, `timeline`, and `json` commands can read current state without adding a new timeline event when no text is provided.

Pending:

- real API context activation;
- UI/dashboard;
- PDF/DOCX export;
- QwenPaw/Discord live import and channel test.

## API Status

Implemented as optional wrappers:

- BMKG weather forecast;
- BMKG latest earthquake;
- BMKG warning CAP feed;
- PetaBencana reports;
- PetaBencana floods.

Not enabled by default.

## QwenPaw Status

Prepared, not installed:

- `qwenpaw_skill/sarflow/`
- `sarflow_qwenpaw_skill.zip`
- `qwenpaw_workspace/SARFLOW.md`
- `QwenPaw_SARFlow_Start.md`

Next QwenPaw task:

1. Disable/remove `BOOTSTRAP.md`.
2. Enable `SARFLOW.md`.
3. Import `sarflow_qwenpaw_skill.zip`.
4. Test with Discord trigger `SARFLOW INTAKE:`.
