# API Sources for SARFlow

These sources are useful for contextual data. They should support briefing and situational awareness only. They must not be used as the sole basis for field decisions.

## PetaBencana Open API

Docs:
https://docs.petabencana.id/routes

Relevant endpoints:
- `/reports`: crowdsourced disaster reports. The docs describe live reports and note that default reports cover the last 3 hours.
- `/floods`: current flood area status. Flood states use numeric severity codes.
- `/floodgauges`: live flood gauge reports, documented for Jakarta.
- `/reports/timeseries`: time series of crowdsourced reports.
- `/floods/timeseries`: time series of flooded areas.
- `/stats/*`: summary statistics.

Potential SARFlow usage:
- Show contextual disaster reports near a flood-related incident.
- Add a "nearby public disaster reports" card in the briefing.
- Add flood severity context if the incident is a flood case.

Implementation note:
- The `/reports` docs ask clients to include a User-Agent header.

## BMKG Open Weather Data

Docs:
https://data.bmkg.go.id/prakiraan-cuaca/

Relevant data:
- Weather forecast for villages/subdistrict-level locations using `adm4`.
- JSON format.
- Forecast covers 3 days.
- One day contains 8 forecast entries, every 3 hours.
- Updated twice daily.
- Access limit documented as 60 requests per minute per IP.
- BMKG must be credited as the data source in the app/system.

Potential SARFlow usage:
- Add weather context to incident briefing.
- Flag weather as "context from BMKG, verify with field team".
- Avoid using forecast as an evacuation instruction.

Example endpoint:

```text
https://api.bmkg.go.id/publik/prakiraan-cuaca?adm4={kode_wilayah_tingkat_iv}
```

## BMKG Earthquake Data

Docs:
https://data.bmkg.go.id/gempabumi/

Relevant data:
- Latest earthquake.
- M 5.0+ earthquake list.
- Felt earthquake list.
- Tsunami-potential earthquake data.

Potential SARFlow usage:
- Context card for earthquake-related reports.
- Do not treat as SAR case verification unless confirmed by officer.

## BMKG Weather Early Warning / CAP

Docs:
https://data.bmkg.go.id/peringatan-dini-cuaca/

Relevant data:
- Weather early warning / nowcast.
- CAP XML format.
- Province RSS feed and detail CAP XML.

Potential SARFlow usage:
- Add weather warning context to briefing.
- Label as external context with attribution.

## Satu Peta MKG

Docs:
https://gis.bmkg.go.id/portal/dataapi

Relevant data:
- Map/API layers for meteorology, climatology, and geophysics.
- Includes rainfall, wind potential, seismicity, and fire danger related layers.

Potential SARFlow usage:
- Add map layers for advanced demo.
- Use as contextual visual data if there is enough build time.

## BNPB Satu Data

Portal:
https://data.bnpb.go.id/

Potential API:
The portal is CKAN-based. Public CKAN-style endpoints are indexed at:
https://data.bnpb.go.id/api/3

Potential SARFlow usage:
- Historical disaster datasets.
- Background risk context.
- Dataset-driven maps in future versions.

Important limitation:
- This is better for historical/reference context than real-time SAR operations.

## PVMBG / MAGMA Indonesia

Docs/source:
https://magma.esdm.go.id/

Potential SARFlow usage:
- Official manual reference for volcano status and eruption information.
- Use for future volcano context only after confirming a stable official API endpoint.

Important limitation:
- Do not scrape pages or rely on undocumented endpoints for MVP.
