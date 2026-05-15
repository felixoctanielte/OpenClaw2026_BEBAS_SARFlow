# SAR SOP Notes - SK KBSN 154

Source file:
`C:\Users\felix\Downloads\scan SK KBSN 154 TENTANG STANDAR PELAYANAN PUBLIK.pdf`

Note: The PDF is scanned, so this file is a manual summary from the visible pages, especially pages 6-8.

## Document Context

Lampiran Keputusan Kepala Badan Nasional Pencarian dan Pertolongan Nomor SK.KBSN-154/HM.01.04/VI/BSN-2020 tentang Standar Pelayanan Publik Badan Nasional Pencarian dan Pertolongan.

Relevant section:
Standar Pelayanan Operasi Pencarian dan Pertolongan.

## Service Delivery - Requirements

Pelapor perlu:
- Memberikan identitas yang jelas.
- Mengetahui atau melaporkan terjadinya kecelakaan/bencana/kondisi membahayakan manusia.
- Memberikan nomor kontak yang dapat dihubungi.
- Menyampaikan informasi kejadian secara jelas.

Implication for SARFlow:
- Intake must collect reporter identity and active contact.
- If location, time, victim count, or reporter contact is missing, SARFlow should mark the report as incomplete and ask follow-up questions.
- The agent should not treat vague reports as fully verified.

## Service Delivery - Mechanism and Procedure

Documented flow from the visible table:
- Pelapor datang langsung atau menghubungi Badan Nasional Pencarian dan Pertolongan through official channels.
- Pelapor melaporkan kejadian kecelakaan, bencana, and/or kondisi membahayakan manusia.
- Petugas menerima dan mencatat laporan.
- Petugas memverifikasi and searches for further information about the incident.
- Search and rescue personnel move toward the incident location to conduct SAR operation.
- Operation result report is delivered to the public/community through official handling.

Implication for SARFlow:
- SARFlow should mirror the administrative sequence: receive, record, verify, brief, log, and draft report.
- SARFlow should maintain verification status per field/event.
- SARFlow should support official review before any public-facing summary is used.

## Time and Cost Notes

Visible page 7 states:
- SAR operation service duration is up to 7 days and may be extended according to applicable regulations.
- SAR operation service for 7 days is not charged.

Implication for SARFlow:
- Timeline and final report can include operation day count.
- The app can flag if a demo operation passes day 7 and needs extension status, but must not decide extension itself.

## Product/Service Scope

Visible service product includes:
- Pencarian.
- Pertolongan.
- Penyelamatan.
- Evakuasi manusia facing emergency/danger in accident, disaster, or condition endangering humans.

Implication for SARFlow:
- The app should frame itself as administrative support for SAR operations, not as an autonomous rescue commander.

## RAG Usage Rules

Use this source to answer:
- What data should be collected from a reporter?
- What is the administrative flow after a report is received?
- What should be logged in the timeline?
- What is the operational service scope?
- What status labels should be shown before verification?

Do not use this source to:
- Choose evacuation method.
- Predict victim location.
- Override field command.
- Publish sensitive victim details.
