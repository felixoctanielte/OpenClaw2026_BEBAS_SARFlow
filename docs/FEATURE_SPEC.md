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

## 5. Multi-turn Update and Conflict Detection

Jika ada update baru, SARFlow harus:
- membaca state insiden sebelumnya;
- mengisi field yang tadinya kosong;
- tidak menimpa data penting yang berbeda secara diam-diam;
- mencatat konflik seperti perubahan jumlah korban, lokasi, kontak, atau waktu terakhir.

Contoh konflik:

```text
victim_count: sebelumnya 2, update masuk 3
```

Konflik harus diberi status:

```text
needs_officer_resolution
```

## 6. External Context Cards

API eksternal bersifat opsional.

Context card harus berisi:
- sumber;
- tipe context;
- status: `ok`, `disabled`, `skipped`, atau `error`;
- ringkasan;
- trust label: `external_context_not_case_fact`.

Context card tidak boleh diperlakukan sebagai fakta kasus.

## 7. Draft Report

Draft laporan berisi:
- identitas insiden;
- ringkasan kondisi;
- timeline;
- informasi terkonfirmasi dari laporan awal;
- informasi yang masih kurang;
- konflik data;
- context eksternal bila digunakan;
- catatan safety.

Draft selalu diberi label:

```text
Draft administratif - perlu verifikasi petugas.
```
