# SARFlow Roadmap

## Phase 0 - Product Framing

Status: done.

Output:
- problem statement;
- safety boundary;
- MVP 4 fitur;
- SOP/RAG direction.

## Phase 1 - Core Agent Runtime

Status: in progress.

Target:
- chat text masuk ke orchestrator;
- extraction menjadi JSON insiden;
- missing field terdeteksi;
- follow-up question keluar;
- briefing dan timeline terbentuk;
- draft laporan bisa dibuat.

Checklist:
- perkuat extraction untuk `pendaki_hilang`;
- perkuat extraction untuk `gunung_meletus`;
- tambah skenario `banjir`;
- tambah skenario `kecelakaan_air`;
- tambah field `pelapor tiba-tiba hilang/tidak bisa dihubungi`;
- tambah field baju/jaket/celana korban;
- tambah test untuk semua skenario.

## Phase 2 - RAG SOP

Status: partial.

Target:
- RAG membaca SOP SK KBSN 154;
- RAG memberi checklist intake;
- RAG menjaga guardrail briefing;
- RAG membantu draft laporan.

Checklist:
- chunk knowledge base per topik;
- tambah source metadata;
- tampilkan source label di briefing;
- pastikan RAG tidak memberi keputusan evakuasi.

## Phase 3 - API Context

Status: planned.

Target:
- API hanya memberi context, bukan keputusan.

Prioritas:
1. BMKG prakiraan cuaca untuk context cuaca.
2. BMKG peringatan dini cuaca untuk nowcast.
3. PetaBencana reports untuk laporan publik sekitar area.
4. BNPB Satu Data untuk data historis.
5. PVMBG/MAGMA sebagai rujukan manual untuk gunung api jika belum ada API resmi yang jelas.

## Phase 4 - Demo Experience

Status: planned.

Target:
- demo 2-3 menit bisa jalan lancar;
- skenario utama: gunung meletus atau pendaki hilang;
- output mudah dibaca juri.

Checklist:
- siapkan 3 input chat dummy;
- siapkan output briefing;
- siapkan output timeline;
- siapkan output draft report;
- pastikan semua ada label verifikasi.

## Phase 5 - QwenPaw + Discord

Status: later.

Target:
- import skill SARFlow;
- pasang persona SARFlow;
- Discord menjadi channel intake;
- command atau trigger `SARFLOW INTAKE:` berjalan.

Catatan:
QwenPaw setup dilakukan setelah core runtime dan demo story stabil.

## Phase 6 - Polish Submission

Status: planned.

Output:
- README reproducible;
- pitch deck PDF;
- demo video;
- public GitHub repo;
- Devpost description.

