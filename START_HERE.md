# SARFlow - Start Here

Ini dokumen utama untuk merapikan arah kerja SARFlow. Untuk sekarang, **QwenPaw setup ditunda dulu**. Fokus kita adalah membuat produk, alur, data, dan runtime SARFlow rapi.

## Tujuan Produk

SARFlow membantu KOM/petugas piket SAR menangani laporan bencana dari chat tidak terstruktur dengan cara:

1. Mengumpulkan data minimum laporan.
2. Mengkategorisasi jenis kejadian.
3. Mengekstrak data penting.
4. Menandai informasi yang kurang.
5. Membuat pertanyaan follow-up.
6. Membuat briefing insiden.
7. Mencatat timeline.
8. Membuat draft laporan.

## Posisi Aman

SARFlow bukan AI pencari korban dan bukan komando operasi. SARFlow adalah **agent administratif**.

AI tidak:
- mengambil keputusan evakuasi final;
- menggantikan komando lapangan;
- menyebarkan informasi belum terverifikasi;
- mengklaim lokasi korban secara pasti.

## Status Saat Ini

Sudah ada:
- runtime lokal `run_orchestrator.py`;
- modul `intake`, `extraction`, `briefing`, `timeline`, `report`, `rag`, `state`, dan `context`;
- knowledge base SOP plus chunk RAG terstruktur;
- template laporan dan timeline;
- skill QwenPaw awal, tapi setup QwenPaw ditunda;
- test untuk skenario pendaki hilang, gunung meletus, banjir, dan kecelakaan air.

## Urutan Kerja Mulai Sekarang

1. Rapikan core workflow lokal.
2. Kunci schema data insiden.
3. Perkuat extraction untuk banyak skenario.
4. Rapikan briefing dan draft laporan.
5. Tambahkan API context yang aman.
6. Siapkan demo script.
7. Baru integrasi ke QwenPaw + Discord.

## Dokumen Yang Dibaca

- `docs/PROJECT_STRUCTURE.md`: struktur folder dan peran file.
- `docs/ROADMAP.md`: apa yang dikerjakan per fase.
- `docs/API_REQUIREMENTS.md`: API/token yang dibutuhkan.
- `docs/FEATURE_SPEC.md`: detail fitur MVP.
- `docs/DEMO_SCRIPT.md`: skenario demo.

## Jalankan Lokal

```powershell
python -m pip install -r requirements.txt
python run_orchestrator.py --reset --text "Ada laporan gunung meletus di sekitar Desa Sumber, 3 warga belum kembali. Pelapor Budi nomor 081111111111. Korban terakhir terlihat jam 16.30, salah satu pakai baju biru celana hitam."
```

Untuk test:

```powershell
python -m pytest -q
```
