---
source_id: sar_sop_sk_kbsn_154
source_file: scan SK KBSN 154 TENTANG STANDAR PELAYANAN PUBLIK.pdf
page_range: 6-7
topic: verification_status
trust_level: derived_from_sop_flow
---

# Verification Status

Karena dokumen menempatkan verifikasi sebagai langkah setelah laporan diterima dan dicatat, SARFlow harus membedakan status data.

Use labels:

- `confirmed`: disebut jelas dalam laporan atau dikonfirmasi petugas.
- `inferred`: disimpulkan dari teks, perlu konfirmasi.
- `missing`: belum tersedia.
- `conflict`: ada informasi baru yang bertentangan dengan informasi sebelumnya.

SARFlow implication:

- Field `confirmed` tetap harus diverifikasi petugas sebelum dipakai untuk publik.
- Field `inferred`, `missing`, dan `conflict` tidak boleh digunakan sebagai fakta final.
- Briefing harus selalu menyebut `Belum terverifikasi - perlu konfirmasi petugas`.

