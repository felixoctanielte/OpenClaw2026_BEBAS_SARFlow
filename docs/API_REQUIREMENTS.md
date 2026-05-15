# API Requirements

API di SARFlow hanya dipakai untuk **context administratif**. API tidak boleh dipakai sebagai dasar keputusan evakuasi final.

## Required For MVP

| API/Token | Dipakai Untuk | Key Dibutuhkan | Status |
|---|---|---:|---|
| LLM provider di QwenPaw | reasoning, extraction, briefing | Ya, kecuali local model | Nanti saat QwenPaw setup |
| Discord Bot Token | channel chat intake | Ya | Nanti saat QwenPaw setup |

Untuk runtime lokal saat ini, belum wajib memakai API eksternal.

## Recommended For Demo Context

| API | Endpoint/Source | Dipakai Untuk | Key | Catatan |
|---|---|---|---:|---|
| BMKG Prakiraan Cuaca | `https://api.bmkg.go.id/publik/prakiraan-cuaca?adm4={kode_adm4}` | context cuaca lokasi kejadian | Tidak untuk endpoint publik | Wajib atribusi `Sumber: BMKG`; batas 60 request/menit/IP. |
| BMKG Peringatan Dini Cuaca | `https://www.bmkg.go.id/alerts/nowcast/id` | nowcast/peringatan dini cuaca | Tidak | Format CAP XML; cocok untuk red-flag cuaca. |
| BMKG Gempabumi | `https://data.bmkg.go.id/DataMKG/TEWS/autogempa.json` dan varian data gempa | context gempa/tsunami | Tidak | Data gempa publik BMKG, update setiap kejadian. |
| PetaBencana Reports | `https://api.petabencana.id/reports` | laporan publik sekitar area | Tidak | Harus kirim `User-Agent`; data urun-daya tidak otomatis valid untuk kasus SAR. |
| PetaBencana Floods | `https://api.petabencana.id/floods` | context banjir | Tidak untuk Open API | Untuk kasus banjir/demo hidrometeorologi. |
| BNPB Satu Data | `https://data.bnpb.go.id/api/3/action/package_search` | dataset historis/referensi | Tidak untuk public CKAN | Lebih cocok untuk background, bukan real-time. |

## Optional/Future

| API/Source | Dipakai Untuk | Catatan |
|---|---|---|
| Satu Peta MKG | layer peta cuaca, curah hujan, seismisitas, FDRS | Untuk dashboard/map layer bila ada waktu. |
| PVMBG/MAGMA Indonesia | status gunung api dan info letusan | Rujukan resmi gunung api, tetapi belum dipakai otomatis sebelum endpoint/API resmi dipastikan. Gunakan sebagai link rujukan/manual source dulu. |
| Google Maps / Mapbox / OpenStreetMap | geocoding, reverse geocoding, map display | Opsional. Untuk MVP lebih aman minta koordinat/link maps dari pelapor. |

## Rules For API Output

- Label semua data eksternal sebagai `context`, bukan fakta kasus.
- Jangan gabungkan laporan PetaBencana dengan laporan SAR sebagai fakta terverifikasi.
- Untuk BMKG, tampilkan atribusi `Sumber: BMKG`.
- Untuk BMKG, jangan scraping halaman web; gunakan endpoint API resmi.
- Kalau API gagal, agent tetap jalan dengan mode manual.

## Implemented Wrapper Functions

File: `modules/api_clients.py`

- `fetch_bmkg_weather(adm4)`
- `fetch_bmkg_latest_earthquake()`
- `fetch_bmkg_weather_warning_cap()`
- `fetch_petabencana_reports(disaster, admin)`
- `fetch_petabencana_floods(admin)`

These wrappers are not enabled by default. They are called only when a future context feature enables them through `agent-config.yml` and CLI flags.

## Sources Checked

- BMKG Prakiraan Cuaca: https://data.bmkg.go.id/prakiraan-cuaca/
- BMKG Gempabumi: https://data.bmkg.go.id/gempabumi/
- BMKG Peringatan Dini Cuaca: https://data.bmkg.go.id/peringatan-dini-cuaca/
- BMKG Terms of Use: https://www.bmkg.go.id/ketentuan-penggunaan
- PetaBencana Open API: https://docs.petabencana.id/routes
- PetaBencana Reports: https://docs.petabencana.id/master-1/routes/crowdsourced-reports
- BNPB Satu Data: https://data.bnpb.go.id/
- Satu Peta MKG: https://gis.bmkg.go.id/portal/dataapi
