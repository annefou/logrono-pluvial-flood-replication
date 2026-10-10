# FOLLOW-UP — climate change and adaptation scenarios for Logroño

**Created 2026-10-10:** [annefou/logrono-flood-adaptation-scenarios](https://github.com/annefou/logrono-flood-adaptation-scenarios) — its `DISCOVERY.md` carries this plan forward (method library pinned at building-climate-risk v0.2.1).

Written 2026-10-10, at the end of Phase 3 of this replication. It is the handoff for
a **separate repository** (create it from `forrt-replication-template`; this file then
becomes its `DISCOVERY.md`). Everything below was checked in this session; re-verify
before it goes into a nanopub draft.

## Why a separate repository

- **Different claim, different chain.** This repo tests the paper's accuracy claim
  (paper-rooted chain, Outcome *partially supported*). The follow-up asks a new question,
  so it gets its own question-rooted chain (PICO), e.g. *"In Logroño, do the planned
  nature-based solutions reduce the number of residents in high pluvial-flood-risk
  buildings under present and future 100-year rainfall, compared with no measures?"*
- **The replication stays frozen** at the release its Outcome cites.
- **Different access.** The replication uses open data only (no credentials); DestinE
  generation-2 data need *upgraded access* (Polytope credentials, CI secrets).

## What to reuse (don't copy)

- **Method**: `building-climate-risk` (github.com/annefou/building-climate-risk), pinned by
  tag; concept DOI 10.5281/zenodo.23282970 (v0.2.0: 10.5281/zenodo.23282971). Hazard-agnostic
  core + `hazards.pluvial`; Hamburg regression 37/37.
- **Logroño inputs**: this repo's release (Zenodo, once minted) — download it and run its
  `01_data_download` + `02_data_clean` to get `data/interim/logrono.gpkg` (buildings with
  residents and census proxies, Cadastre block-gap streets, Urban Atlas water, impact
  places). Results of this repo: hazard at reported places is strongly supported
  (83.8th percentile among 512 streets, p ≤ 0.0001), risk indices only weakly.
- **Climate DT extraction**: `annefou/extreme-precipitation-climatedt-replication`
  (Polytope polygon feature on HEALPix level 10, `avg_tprate`, `stream=clte`, IFS-NEMO
  SSP3-7.0, 1991–2010 vs 2030–2049, return levels by duration). Consider moving it into a
  shared library too.

## Data — verified sources

### REACHOUT scenarios (already in `PluvialFloodMap_Logrono.zip`, Zenodo 10.5281/zenodo.14035876)
Embedded metadata (SaferRAIN, 15-min uniform rain, Green-Ampt, no storage tanks), RP100:

| Folder | Rain (RP100) | Infiltration layer |
|---|---|---|
| `Baseline` | 26.77 mm | `32632_Logrono_PERM_sr` |
| `Baseline_CC_Q50` / `_Q90` | 31.25 mm (+17 %) / 38.99 mm (+46 %) | same |
| `NBSplanned` | 26.77 mm | `NBSPlanned_PERM_sr` |
| `NBSplanned_plus` | 26.77 mm | `NBSPlanned_PERM_sr` (**metadata identical to NBSplanned** — find the difference in REACHOUT documentation before interpreting) |
| `Allgreen` | 26.77 mm | `32632_Logrono_PERM_sr_NBStest` |
| `*_CC_Q50` / `*_CC_Q90` | 31.25 / 38.99 mm | per scenario |

- **Grids differ**: Baseline and Allgreen 8230 × 9604; the CC and NBS rasters 5696 × 8002 —
  compare on the common footprint only.
- **Defect**: `Allgreen_CC_Q90/D_RP25_Q90.tif` is 0 bytes in the archive (report to the authors,
  with the EPSG:32632 labelling).

### Destination Earth (checked 2026-10-10)
- **Climate DT storylines** (released 18 May 2026): continuous simulations "from 2017 to the
  present", IFS-FESOM ~10 km, large-scale circulation nudged to ERA5 above the boundary layer,
  in three climates — 1950s-like, present, +2 °C (~2050s); five members per scenario (news
  item). All four Logroño storms (2018-09-17, 2021-09-01, 2023-06-21, 2024-10-16) fall inside.
  Lets us ask how much heavier the *actual* storms would be at +2 °C. Precedents: Valencia
  DANA 2024 (egusphere-2025-5929), Central European floods 2024. Output frequency for the
  storylines is not stated — check on the platform. Sources: GMD 19, 2821, 2026
  (https://gmd.copernicus.org/articles/19/2821/2026/); https://destine.ecmwf.int/news/new-destine-climate-digital-twin-simulations-available/
- **Climate DT generation-2 projections**: 1990–2049, ~5 km, hourly, ICON + IFS-FESOM +
  IFS-NEMO (three-model spread), HEALPix; DOI 10.21957/79c6af3105. Cross-check of REACHOUT's
  EURO-CORDEX uplift (+17 % / +46 %).
- **Impact-sector indicators** (extreme precipitation, hydrology): announced 18 May 2026 for
  "the coming months" — release not confirmed; check the platform.
- **Not usable here**: Extremes DT on-demand 500–750 m runs (forecasts for selected events);
  the "Precipitation-to-Flood Signals" pilot (Italy only, river flooding); the "Disaster Risk
  Mitigation & Climate Adaptation" use case (Deltares; coastal/compound; Basque Country, UK,
  Philippines, La Réunion, BES) — but its open tools SFINCS (fast flood model incl. pluvial)
  and Delft-FIAT (building damage) are candidates for an alternative hazard model and an
  economic-damage complement.

## Method points that must be handled

1. **Fix the class breaks from the baseline.** The authors' iterated-mean classes are relative
   to each map's own distribution; recomputing them per scenario can hide a uniform increase.
   Compare absolute risk, or classes with baseline breaks.
2. **Scenarios, not predictions** — conditional on design storms.
3. **15 min vs hourly**: Climate DT gives hourly at best; use relative changes (deltas), never
   absolute grid-cell values, and state the sub-hourly scaling assumption.
4. **Storylines at ~10 km** cannot place a convective cell on a street: compare regional
   event maxima (e.g. heaviest 1–3 h around Logroño) as ratios between climates; map the
   scaled storm to the REACHOUT return period with the matching rainfall (approximation).
5. **Return levels from 20-year windows**: RP2–RP25 are robust, RP100 is a long extrapolation.
6. **People fixed at 2021** unless INE population projections are added.
7. **No sewer network** in SaferRAIN; NBS only as infiltration change.
8. **Optional add-on (agreed 2026-10-10)**: aggregate risk, flooded share and impacts to
   HEALPix (healpix-geo, WGS84 ellipsoid, NESTED; level ~17), written as GRID4EARTH / EOPF Zarr.

## Suggested plan
- Phase 1 — PICO question (question-rooted chain); optionally cite this replication's chain.
- Phase 2 — reuse this repo's release for inputs; REACHOUT scenarios; Climate DT storylines and
  projections via Polytope (credentials as CI secrets).
- Phase 3 — residents in high risk (baseline breaks) per scenario; where the NBS help; whether
  the 2018–2024 impact places benefit; storyline uplift of the four observed storms.
