# QwenPaw Import Checklist

Use this after local SARFlow runtime is validated.

## Files To Use

- Persona: `qwenpaw_workspace/SARFLOW.md`
- Skill zip: `sarflow_qwenpaw_skill.zip`
- Skill folder fallback: `qwenpaw_skill/sarflow/`

## Steps

1. Open QwenPaw Console.
2. Go to `Workspace -> Files`.
3. Disable or delete `BOOTSTRAP.md` if QwenPaw still enters bootstrap mode.
4. Add/enable `SARFLOW.md` using `qwenpaw_workspace/SARFLOW.md`.
5. Go to `Workspace -> Skills`.
6. Import `sarflow_qwenpaw_skill.zip`.
7. Enable skill `sarflow`.
8. Test in Discord or Chat:

```text
SARFLOW INTAKE:
Ada banjir di Desa Melati, 5 warga terjebak di rumah.
Pelapor Andi nomor 081222333444. Air naik sejak jam 20.15,
akses jalan utama tertutup.
```

## Expected Behavior

SARFlow should return:

- structured incident summary;
- missing fields;
- administrative priority;
- max 3 follow-up questions;
- safety label;
- no final evacuation decision.

## Common Problem

If the bot asks about your profile/name instead of SARFlow, it is still loading `BOOTSTRAP.md`.

Fix:

- disable/remove `BOOTSTRAP.md`;
- enable `SARFLOW.md`;
- retry with `SARFLOW INTAKE:`.

