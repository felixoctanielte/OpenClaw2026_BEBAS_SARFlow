---
source_id: sarflow_policy
source_file: internal_design
topic: external_context_rules
trust_level: project_guardrail
---

# External Context Rules

External APIs such as BMKG, PetaBencana, BNPB, and Satu Peta MKG are context sources only.

Rules:

- Label API data as `context`, not verified case fact.
- Do not merge public disaster reports into official SAR case facts.
- If API fails, continue manual intake.
- Always include attribution where required, especially BMKG.
- Do not use API context to produce evacuation commands.

