# Demo Script

## Demo Goal

Menunjukkan bahwa SARFlow membantu KOM merapikan laporan bencana yang tidak lengkap menjadi data, briefing, timeline, dan draft laporan.

## Scenario A - Gunung Meletus

Input:

```text
SARFLOW INTAKE:
Ada laporan gunung meletus di sekitar Desa Sumber, 3 warga belum kembali.
Pelapor Budi nomor 081111111111. Korban terakhir terlihat jam 16.30,
salah satu pakai baju biru celana hitam.
```

Expected output:
- jenis kejadian: `gunung_meletus`;
- lokasi: `sekitar Desa Sumber`;
- jumlah korban: `3`;
- pelapor: `Budi / 081111111111`;
- waktu terakhir: `16:30 WIB`;
- pakaian: `baju biru, celana hitam`;
- missing: `koordinat/link maps`;
- prioritas administratif: `Tinggi`;
- follow-up: minta koordinat/link maps.

## Scenario B - Pendaki Hilang

Input:

```text
SARFLOW INTAKE:
Mas, ada 2 pendaki belum turun dari Pos 3 Gunung Lawu. Terakhir kontak jam 18.10.
Logistik tinggal sedikit, hujan, sinyal putus. Pelapor teman rombongan, nomor 081234567890.
```

Expected output:
- jenis kejadian: `pendaki_hilang`;
- lokasi: `Pos 3 Gunung Lawu`;
- jumlah korban: `2`;
- waktu terakhir: `18:10 WIB`;
- kondisi: `logistik tinggal sedikit, sinyal putus`;
- missing: koordinat/link maps dan pakaian terakhir;
- prioritas administratif: `Tinggi`.

## Scenario C - Banjir

Input:

```text
SARFLOW INTAKE:
Ada banjir di Desa Melati, 5 warga terjebak di rumah.
Pelapor Andi nomor 081222333444. Air naik sejak jam 20.15,
akses jalan utama tertutup.
```

Expected output:
- jenis kejadian: `banjir`;
- lokasi: `Desa Melati`;
- jumlah korban: `5`;
- pelapor: `Andi / 081222333444`;
- waktu: `20:15 WIB`;
- kondisi: `terjebak, air naik`;
- akses: `akses jalan utama tertutup`;
- missing: `koordinat/link maps` dan pakaian bila korban belum teridentifikasi.

## Scenario D - Kecelakaan Air

Input:

```text
SARFLOW INTAKE:
Laporan perahu nelayan mati mesin di Perairan Tanjung Pasir.
Ada 2 nelayan di kapal, terakhir kontak jam 05.20.
Pelapor Sari nomor 081555666777, gelombang tinggi dan arus deras.
```

Expected output:
- jenis kejadian: `kecelakaan_air`;
- lokasi: `Perairan Tanjung Pasir`;
- jumlah korban: `2`;
- pelapor: `Sari / 081555666777`;
- waktu terakhir kontak: `05:20 WIB`;
- kondisi: `perahu mati mesin`;
- cuaca/lapangan: `gelombang tinggi, arus deras`;
- prioritas administratif: `Tinggi` atau `Kritis`.

## Demo Flow

1. Jalankan input awal.
2. Tunjukkan extracted data.
3. Tunjukkan missing fields.
4. Tunjukkan pertanyaan follow-up.
5. Tunjukkan briefing.
6. Tunjukkan timeline.
7. Generate draft report.

## Safety Line For Pitch

SARFlow tidak mengambil keputusan evakuasi final. Semua output adalah rekomendasi administratif untuk diverifikasi petugas.
