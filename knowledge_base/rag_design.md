# SARFlow RAG Design

## Goal

RAG should make SARFlow more grounded, auditable, and safe. It should not make the agent more aggressive in making operational decisions.

## Knowledge Collections

### `sar_sop`

Sources:
- SK KBSN 154 service delivery notes.
- Internal or public SOP summaries.
- Intake requirements.
- Service procedure.
- Reporting/timeline expectations.

Used by:
- Intake Agent.
- Risk Briefing Agent.
- Timeline Report Agent.

### `report_templates`

Sources:
- Incident briefing templates.
- Final report draft templates.
- Timeline event taxonomy.

Used by:
- Risk Briefing Agent.
- Timeline Report Agent.

### `public_education`

Sources:
- Safe public information about Basarnas/SAR role.
- FAQ for Gen Z/millennial audience.

Used by:
- Optional "Kenali Basarnas" mode.
- Not used in emergency triage.

### `external_context`

Sources:
- PetaBencana API summaries.
- BMKG weather summaries.
- BNPB historical context.

Used by:
- Context cards in incident briefing.
- Never used as final command.

## Chunking Strategy

Chunk by meaning, not by fixed page only:
- Requirements.
- Intake procedure.
- Verification procedure.
- Reporting procedure.
- Safety/communication restrictions.
- Report templates.

Suggested metadata:

```json
{
  "source": "SK KBSN 154",
  "page": 7,
  "section": "Service Delivery",
  "topic": "verification_flow",
  "trust_level": "official_scan_manual_summary"
}
```

## Retrieval Points

### During Chat Intake

Query:
`data minimum laporan SAR, identitas pelapor, kontak, lokasi, waktu, korban`

Output:
- Missing field checklist.
- Next 2-3 follow-up questions.

### During Triage

Query:
`red flag korban hilang, cuaca, logistik, usia rentan, lokasi bahaya`

Output:
- Risk factors.
- Administrative priority.
- Verification tasks.

### During Briefing

Query:
`format ringkasan insiden SAR, status verifikasi, informasi belum lengkap`

Output:
- Incident briefing.
- Caveat: "Belum terverifikasi".

### During Timeline/Final Report

Query:
`alur menerima mencatat memverifikasi laporan operasi pencarian pertolongan`

Output:
- Timeline event labels.
- Draft report structure.

## Guardrail Prompt Snippet

```text
You are SARFlow, an administrative SAR co-pilot for officers.
Use retrieved SOP only to support intake, verification, briefing, timeline logging, and report drafting.
Do not decide evacuation, do not replace field command, do not publish unverified information, and do not claim victim location certainty.
Every output must separate confirmed, inferred, and missing information.
If information is incomplete, ask concise follow-up questions.
```

## Minimal RAG Implementation

For hackathon speed:
- Store chunks as Markdown files.
- Load and embed chunks at app start.
- Use Chroma, FAISS, LanceDB, or Supabase pgvector.
- Retrieve top 3-5 chunks per task.
- Pass retrieved context to the agent prompt.
- Show source labels in the UI.

Fallback if vector DB takes too long:
- Use keyword retrieval over Markdown chunks.
- Still call it "retrieval-augmented" transparently as a simple retriever.
- Upgrade to vector embeddings if time remains.

## Evaluation Checklist

Good RAG behavior:
- Agent asks for reporter contact if missing.
- Agent asks for last seen time and precise location.
- Agent labels unverified claims.
- Agent cites SOP/source snippets in briefing notes.
- Agent refuses to make evacuation command.

Bad RAG behavior:
- Agent invents facts.
- Agent treats public reports as verified case facts.
- Agent recommends tactical evacuation steps.
- Agent exposes sensitive victim information in a public summary.
