# Start Plan - SARFlow on QwenPaw + Discord

## Starting Point

Karena Discord bot sudah disiapkan, jangan mulai dari bikin bot baru. Mulai dari:

1. Buat satu agent/persona bernama `KOM - SARFlow`.
2. Pasang skill `sarflow` ke workspace agent itu.
3. Pakai Discord sebagai channel intake laporan.
4. Demo dengan 1 skenario dummy: pendaki hilang.

Current prepared files:

- `qwenpaw_workspace/SARFLOW.md`
- `qwenpaw_skill/sarflow/`
- `sarflow_qwenpaw_skill.zip`
- `STATUS_REPORT.md`

## How QwenPaw Fits

QwenPaw punya tiga bagian yang relevan:

- **Channel**: Discord, tempat laporan masuk dan output dikirim.
- **Persona**: aturan perilaku agent, misalnya "kamu adalah KOM SARFlow".
- **Skill**: kemampuan khusus SARFlow, berisi SOP, schema, risk rules, dan script/tool.

Untuk SARFlow, fokusnya:

```text
Discord message
-> QwenPaw Agent Persona: KOM - SARFlow
-> sarflow skill
-> extract incident data
-> check SOP/RAG references
-> risk triage
-> briefing
-> timeline log
-> draft report
```

## Minimum Setup Checklist

### 0. Fix Bootstrap Mode Kalau QwenPaw Nyasar

Kalau QwenPaw membalas seperti:

```text
BOOTSTRAP MODE `BOOTSTRAP.md` exists - first-time setup.
Tell me a bit about yourself...
```

artinya agent belum memakai persona SARFlow. Solusinya:

1. Buka QwenPaw Console.
2. Masuk `Workspace -> Files`.
3. Cari `BOOTSTRAP.md`.
4. Disable dari system prompt atau hapus setelah setup awal selesai.
5. Tambahkan/enable `SARFLOW.md` dari folder `qwenpaw_workspace/SARFLOW.md`.
6. Pastikan `AGENTS.md`, `SOUL.md`, `PROFILE.md`, dan `SARFLOW.md` yang aktif, bukan `BOOTSTRAP.md`.

Setelah itu coba lagi dari Discord dengan awalan:

```text
SARFLOW INTAKE:
```

### 1. Confirm Discord Bot Works

Di Discord, pastikan bot bisa membalas pesan biasa.

Contoh:

```text
@bot halo, jawab singkat
```

Kalau tidak membalas:
- Pastikan Discord `Message Content Intent` aktif di Discord Developer Portal.
- Pastikan channel Discord di QwenPaw enabled.
- Pastikan token bot benar.
- Pastikan bot punya permission `Send Messages`.

### 2. Create SARFlow Persona

Di QwenPaw Console:

```text
Agent -> Workspace -> edit/create Markdown persona file
```

Tambahkan file persona, misalnya `SARFLOW.md`, lalu enable file itu.

Isi pendek:

```markdown
# SARFlow Persona

Kamu adalah KOM - SARFlow, AI co-pilot administratif untuk petugas piket SAR.
Tugasmu membantu intake laporan, ekstraksi data, briefing insiden, triage administratif awal, timeline, dan draft laporan.

Kamu tidak boleh:
- mengambil keputusan evakuasi final;
- menggantikan komando lapangan;
- menyebarkan informasi belum terverifikasi;
- mengklaim lokasi korban secara pasti.

Selalu pisahkan informasi confirmed, inferred, dan missing.
Jika laporan belum lengkap, tanyakan maksimal 3 pertanyaan follow-up paling penting.
Semua output harus diberi status verifikasi.
```

### 3. Install SARFlow Skill

Aku sudah siapkan draft skill di:

```text
qwenpaw_skill/sarflow/
```

Cara paling mudah:

1. Buka QwenPaw Console.
2. Masuk `Workspace -> Skills`.
3. Create skill baru bernama `sarflow`.
4. Copy isi `qwenpaw_skill/sarflow/SKILL.md`.
5. Kalau mau file lengkap, salin folder `qwenpaw_skill/sarflow/` ke:

```text
~/.qwenpaw/workspaces/default/skills/sarflow/
```

Di Windows path biasanya:

```text
C:\Users\felix\.qwenpaw\workspaces\default\skills\sarflow\
```

Lalu enable skill di Console.

Recommended:

- Import `sarflow_qwenpaw_skill.zip` through QwenPaw UI if possible.
- If zip import fails, copy folder `qwenpaw_skill/sarflow/` manually to the workspace skills folder.

Kalau agent id kamu bukan `default`, pakai folder agent itu:

```text
C:\Users\felix\.qwenpaw\workspaces\{agent_id}\skills\sarflow\
```

### 4. Test Prompt in Discord

Kirim ini ke Discord:

```text
@KOM /sarflow
Mas, ada 2 pendaki belum turun dari Pos 3 Gunung Lawu. Terakhir kontak jam 18.10.
Logistik tinggal sedikit, hujan, sinyal putus. Pelapor teman rombongan, nomor 08xxxx.
```

Expected output:
- Ringkasan insiden.
- Extracted fields.
- Missing fields.
- Risk triage administratif.
- Follow-up questions.
- Timeline event pertama.

### 5. Demo Script

Urutan demo 2-3 menit:

1. Tunjukkan Discord chat masuk.
2. Bot mengekstrak data dan menandai missing fields.
3. Bot menanyakan follow-up: koordinat, pakaian terakhir, identitas korban.
4. Masukkan jawaban follow-up.
5. Bot update briefing dan timeline.
6. Bot generate draft laporan akhir.

## Recommended Discord Commands

Gunakan command sederhana agar demo rapi:

```text
/sarflow intake <laporan>
/sarflow update <info baru>
/sarflow briefing
/sarflow timeline
/sarflow report
```

Kalau belum sempat bikin command parser khusus, cukup pakai kata kunci:

```text
@KOM SARFLOW INTAKE: ...
@KOM SARFLOW UPDATE: ...
@KOM SARFLOW BRIEFING
@KOM SARFLOW REPORT
```

## Hackathon Scope

Wajib jadi:
- Discord intake.
- Structured extraction.
- Missing-field follow-up.
- Risk briefing.
- Timeline.
- Draft report.
- RAG/SOP references dari file Markdown.

Bonus:
- BMKG weather context.
- PetaBencana context.
- Dashboard web.

Jangan dikerjakan dulu:
- WhatsApp asli.
- Prediksi lokasi korban.
- Routing evakuasi.
- Auth kompleks.

## Local Runtime Before QwenPaw

Before importing into QwenPaw, verify locally:

```powershell
python -m pytest -q
python run_orchestrator.py --reset --command intake --text "Ada banjir di Desa Melati, 5 warga terjebak di rumah. Pelapor Andi nomor 081222333444. Air naik sejak jam 20.15, akses jalan utama tertutup."
```

## Sources

QwenPaw official references:
- GitHub: https://github.com/agentscope-ai/QwenPaw
- Skills docs: https://qwenpaw.agentscope.io/docs/skills/
- Channels docs: https://qwenpaw.agentscope.io/docs/channels/
- Config docs: https://qwenpaw.agentscope.io/docs/config/
