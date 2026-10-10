# Recorded flood impacts — Logroño

Curated by hand from local press reports and versioned here (not downloaded).
Reports say where water caused problems, not who was vulnerable: they test the
hazard (and exposure) components of the risk framework, not social vulnerability.

## `logrono_events.csv` — one row per place and event

- `reported_impact_es` is copied **verbatim** from the source (Spanish); nothing is
  recorded that the source does not say. Each quote was checked by string search
  against the source text on `checked_on`. One normalisation: in the 2024-10-16
  sentence, the PDF text extraction reads "avenidade Burgos"; recorded as
  "avenida de Burgos".
- `event_date` is the day of the storm; `published` the article date (they differ when
  the article reports the previous evening).
- `place_type`: street, road, junction, building, sports_facility.
  "el Adarraga" (2018-09-17) is read as the Centro de Tecnificación Deportiva Javier
  Adarraga (https://www.larioja.org/ctd-javier-adarraga/es). OpenStreetMap's only
  "Adarraga" feature in Logroño is a car park on Paseo de Las Norias (42.47358 N,
  2.45246 W; Nominatim, 2026-10-10) — used as the approximate location of the complex.
  Address confirmed by Anne Fouilloux on Google Maps (2026-10-10): "Adarraga,
  P.º de las Norias, 26006 Logroño, La Rioja" — the same street as the OSM car park
  (OSM gives postcode 26002). Google Maps coordinates are not used (licence).
- `source_kind`: `press` = the article's own reporting; `social_media_embedded` = a
  post embedded in the article (weaker evidence; analyse separately).
- Located in `notebooks/02_data_clean.py`: streets from the Cadastre address register
  (official thoroughfare names + address points); places without an address from
  OpenStreetMap features in `osm_features.json` (ODbL; fetched once by
  `01_data_download.py` with the query stored in the file, then committed).
- Wind damage reported in the same articles (terraces in Portales, a fallen tree in
  calle Lope de Vega, 2018) is excluded: it is not flooding.

## `logrono_event_rainfall.csv` — one row per event

Rainfall and incident counts as reported, for matching each event to a REACHOUT
design storm (15-min events; Logroño RP2 9.79 … RP100 26.77 mm). `rain_reported_es`
is verbatim (two figures in one article are separated by ` | `). Events without
named places (2021-09-01, 2023-09-01, 2024-09-21) appear only here.

## Sources

nuevecuatrouno.com articles serve a Cloudflare challenge to scripted clients; they
were read from PDF prints of the web pages (2026-10-10) that are **not** redistributed
in this repository (copyright). The 2023-06-21 article was read from its Wayback
Machine copy (`archived_url`), and Infobae (2023-06-22) directly.
