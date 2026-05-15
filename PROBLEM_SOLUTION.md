# SARFlow Problem and Solution

## Problem

KOM/petugas piket sering menerima laporan bencana atau kondisi membahayakan manusia dalam bentuk chat yang tidak rapi. Pelapor bisa panik, menjawab tidak lengkap, lalu tiba-tiba tidak bisa dihubungi. Informasi penting seperti data diri pelapor, kontak aktif, lokasi presisi, waktu terakhir korban terlihat, jumlah korban, kondisi korban, dan pakaian terakhir sering tercecer.

Contoh kekurangan informasi:
- data diri dan kontak pelapor belum jelas;
- lokasi kejadian hanya berupa patokan umum;
- korban terakhir terlihat jam berapa belum pasti;
- jumlah korban berubah-ubah;
- ciri korban belum lengkap, termasuk warna baju/jaket dan celana;
- jenis laporan spesifik belum dikategorikan, misalnya pendaki hilang, banjir, kecelakaan air, atau gunung meletus;
- pelapor mengirim chat awal lalu hilang/tidak membalas.

Akibatnya petugas harus mengulang pertanyaan, merapikan data manual, dan menyusun briefing/timeline di tengah kondisi yang harus cepat.

## Solution

SARFlow adalah AI agent administratif untuk membantu KOM menghandle informasi bencana dengan cara:

1. Mengumpulkan data minimum laporan.
2. Mengkategorisasi jenis kejadian.
3. Mengekstrak data insiden dari chat tidak terstruktur.
4. Menandai data yang masih kurang.
5. Membuat pertanyaan follow-up paling penting.
6. Menyusun risk triage administratif awal.
7. Membuat briefing singkat untuk petugas.
8. Mencatat timeline otomatis.
9. Membuat draft laporan spesifik.

## Benefit

Manfaat untuk KOM/petugas:
- intake laporan lebih cepat dan konsisten;
- data kritis tidak gampang terlewat;
- briefing siap dibaca tanpa paragraf panjang;
- timeline operasi tercatat sejak awal;
- draft laporan akhir lebih mudah dibuat;
- petugas tetap memegang keputusan dan verifikasi.

## Safety Position

SARFlow tidak mengambil keputusan evakuasi final, tidak menggantikan komando lapangan, dan tidak menyebarkan informasi yang belum diverifikasi. Semua output adalah rekomendasi administratif untuk diverifikasi petugas.

