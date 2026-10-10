# Recorded flood impacts — Logroño

`logrono_events.csv` lists places in Logroño where press reports describe pluvial
flooding, one row per place and event. It is curated by hand and versioned here.

- `reported_impact_es` is copied **verbatim** from the source (Spanish), so every row
  can be checked against it. Nothing is recorded that the source does not say.
- `source_kind`: `press` = the article's own reporting; `social_media_embedded` = a
  post embedded in the article (weaker evidence; analyse separately).
- `archived_url`: Wayback Machine copy, where one exists.
- Locations are not yet geocoded; geocoding is done in `notebooks/02_data_clean.py`.

Reports say where water caused problems, not who was vulnerable: they test the
hazard (and exposure) components, not social vulnerability.

Coverage so far: 21 June 2023 only. nuevecuatrouno.com serves a Cloudflare challenge
to scripted clients, and the other articles listed in `DISCOVERY.md` (2018-09-17,
2021-09-01, 2023-09, 2024-09, 2024-10-17) have no Wayback copy; they still need to be
read and recorded.
