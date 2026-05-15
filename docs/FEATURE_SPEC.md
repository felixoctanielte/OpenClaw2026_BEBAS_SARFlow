# Feature Spec

## 1. Chat Intake

Input:
- chat laporan dari pelapor atau petugas;
- bisa tidak lengkap dan tidak rapi.

Data yang harus dikumpulkan:
- nama pelapor;
- kontak pelapor aktif;
- hubungan pelapor dengan korban;
- jenis kejadian;
- lokasi kejadian/lokasi terakhir;
- koordinat atau link maps;
- waktu terakhir korban terlihat/kontak;
- jumlah korban;
- kondisi korban;
- pakaian terakhir: baju/jaket dan celana;
- kondisi lapangan/cuaca;
- akses menuju lokasi bila ada.

Output:
- pertanyaan follow-up maksimal 3;
- missing field list;
- status verifikasi.

## 2. Auto Extraction

Output JSON:
- `incident_type`
- `location_text`
- `coordinates`
- `last_seen_time`
- `victim_count`
- `victims`
- `reporter`
- `weather_or_field_condition`
- `missing_fields`
- `red_flags`
- `administrative_priority`
- `verification_status`
- `field_confidence`

## 3. Risk Triage + Briefing

Triage administratif:
- `Rendah`
- `Sedang`
- `Tinggi`
- `Kritis`

Red flag:
- lokasi tidak presisi;
- korban banyak;
- korban anak/lansia/rentan;
- cedera/sakit;
- cuaca/lapangan berisiko;
- logistik/komunikasi terbatas;
- pelapor/korban tidak bisa dihubungi;
- SOS/distress;
- gunung/laut/sungai/hutan/daerah bencana.
- banjir dengan warga terjebak/terisolir;
- kecelakaan air seperti perahu/kapal mati mesin, hanyut, tenggelam, atau terseret arus.

Briefing harus singkat dan bisa dibaca cepat oleh petugas.

## 4. Timeline

Setiap input/update menjadi event:
- waktu;
- sumber;
- jenis event;
- ringkasan;
- status verifikasi.

Timeline menjadi sumber utama untuk draft laporan.

## 5. Draft Report

Draft laporan berisi:
- identitas insiden;
- ringkasan kondisi;
- timeline;
- informasi terkonfirmasi dari laporan awal;
- informasi yang masih kurang;
- catatan safety.

Draft selalu diberi label:

```text
Draft administratif - perlu verifikasi petugas.
```
