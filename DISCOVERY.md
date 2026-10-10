# DISCOVERY — handoff for the Logroño replication

Written 2026-10-10 at the end of the session that produced the Hamburg
reproduction. Everything below was checked in that session (URLs opened, files
downloaded and inspected); treat it as a starting point, and re-verify anything
before it goes into a nanopub draft (`docs/verify-before-drafting.md`).

## What this repository is for

A FORRT **replication** of Vogelbacher et al. (2026), *A high-resolution framework
for urban pluvial flood risk mapping*, NHESS 26:2765–2783,
[doi:10.5194/nhess-26-2765-2026](https://doi.org/10.5194/nhess-26-2765-2026),
applied to **Logroño, Spain** with open Spanish data, and **compared with recorded
flood impacts**.

It **extends** the Hamburg reproduction (prior chain in `CITATION.cff`):

- Repo: [annefou/hamburg-pluvial-flood-replication](https://github.com/annefou/hamburg-pluvial-flood-replication),
  release v0.1.1, version DOI [10.5281/zenodo.23270558](https://doi.org/10.5281/zenodo.23270558).
- Chain (published 2026-10-09, verify_chain green): Quote `RA2rRZOL…`, AIDA `RAg-Em1_…`
  ("Building-level pluvial flood risk is highest for buildings close to flooded areas
  and streets where high exposure and high flood hazard coincide."), Claim `RA5O9-MZ…`,
  Reproduction Study `RAwD-DCU…`, Outcome `RA6V_jAy…` (Validated, high), CiTO
  `RAI00BYTAPLTsNoY19DGNKF04vAjTuVv6K3WbYmo055CA` (confirms).
- `nanopubs/imported/CHAIN_SUMMARY.md` (gitignored; regenerate with `/import-from-nanopub`)
  holds its scope, method, deviations and limitations verbatim.

**Reuse the Hamburg implementation**, not the FAIR2Adapt toolbox: `notebooks/03_analysis.py`
in the Hamburg repo (scenario C) — TOPSIS + entropy social vulnerability, hazard rings that
exclude **all** building footprints, risk = SV_PF × E × H, iterated-mean classes. It
matches the authors' ArcGIS output (37/37 classes). Note what had to be inferred there:
sensitivity weights children 0.3 / elderly singles 0.7 (Eq. 2 and results; the paper's
text says 0.7/0.3), TOPSIS vector normalisation (scripts; Eq. 4 shows a sum), entropy in
all three TOPSIS steps, three iterations for the classes.

## Decisions already taken with Anne

1. **Replication, not reproduction** — new city, new data, two vulnerability proxies, a
   different hazard model. FORRT study type: *Replication Study*; the CiTO should
   `extends` the Hamburg chain (and relate to the paper).
2. **The most interesting test is the comparison with real impacts** (Anne). Also in
   scope: transferability with open Spanish data, and robustness of hotspots to the
   proxies and weights.
3. **Start with the ready-made census proxies**; an INE custom table (children 0–9,
   single-person households 65+, per sección censal) is a later improvement.
4. **Caveat to keep in view:** the generic AIDA ("risk highest where exposure and hazard
   coincide") partly follows from risk = SV × E × H by construction. A meaningful claim
   for Logroño is about transfer and about agreement with observed impacts — choose the
   Quote/AIDA accordingly in Phase 1 (e.g. the paper's transferability statement,
   Sect. 4.3.2, or its qualitative validation against past events, Sect. 4.3.1).
5. **Impacts test the hazard (and exposure), not social vulnerability** — calls and
   incident reports say where water caused problems, not who was vulnerable.

## Data — verified sources

### Hazard: REACHOUT pluvial flood maps
- Staccione, A. and Pal, J. S. (2024). *Urban pluvial flood maps under different green
  cover scenarios*, Zenodo [10.5281/zenodo.14035876](https://doi.org/10.5281/zenodo.14035876),
  CC BY 4.0. **The paper itself cites this dataset** (Sect. 4.3.2) as a basis for transfer.
- `PluvialFloodMap_Logrono.zip` (254 MB; 12.5 GB unzipped — extract only what is needed).
  Sub-folders per scenario: `Baseline`, `Allgreen`, `NBSplanned`, … ; files `A_RP2.tif` …
  `G_RP200.tif`. The `NBSplanned` rasters are 182 MB each (not COG-compressed).
- Inspected `Baseline/F_RP100.tif`: **2 m** pixels, 9604 × 8230 (≈ 19 × 16 km), Float32,
  NoData −9999, COG/DEFLATE, depths 0–14.5 m (mean 0.38). Embedded metadata: SaferRAIN,
  "uniform rain of 26.77mm over all the domain, duration 0.25h, no storage tanks,
  GreenAmpt enabled".
- **CRS is labelled WGS 84 / UTM zone 32N (EPSG:32632)** although Logroño is in zone 30;
  coordinates still place it correctly (42.5° N, 2.4° W) but distances are distorted by
  ~1 % that far from the zone's meridian. Reproject to ETRS89 / UTM 30N (EPSG:25830, the
  Cadastre's CRS) and report it; consider telling the REACHOUT authors.
- Design rainfall (Logroño, 15-min events, from SOS-Logroño station data 1999–2022):
  RP2 9.79, RP5 13.51, RP10 16.27, RP25 20.15, RP50 23.33, **RP100 26.77**, RP200 30.50 mm.
  Climate-change variants (EURO-CORDEX Q50/Q90) are also provided.
- Model differences from Hamburg (deviations): SaferRAIN is hydrostatic fill-and-spill
  with infiltration and **no sewer network**; Hamburg used 2-D hydrodynamic VISDOM coupled
  with SWMM. REACHOUT's record does not describe validation against observed events.

### Buildings: Spanish Cadastre (INSPIRE Buildings)
- Bulk download (ATOM) for Logroño (municipality 26900):
  `https://www.catastro.hacienda.gob.es/INSPIRE/Buildings/26/26900-LOGRO%C3%91O/A.ES.SDGC.BU.26900.zip`
  (6 MB; dated 2026-08-21; CC BY 4.0; EPSG:25830). The WFS returned an HTML error page —
  use the ATOM files. Feed: `https://www.catastro.hacienda.gob.es/INSPIRE/buildings/ES.SDGC.BU.atom.xml`.
- `building.gml`: 6,327 buildings with `currentUse` (e.g. `1_residential`, `3_industrial`),
  `numberOfDwellings`, `numberOfBuildingUnits`, gross floor area (`value`, m²).
- `buildingpart.gml`: 36,977 parts with `numberOfFloorsAboveGround`, `numberOfFloorsBelowGround`.
- Gap: no per-floor use in the open data → whether a ground floor is residential needs an
  assumption (the paper's mixed-use rule) or the protected cadastral unit data.
- Advantage over the paper: dwellings per building → residents can be allocated per
  dwelling, not only by floor area.

### Vulnerability: INE Census 2021 per sección censal
- Indicators: `https://www.ine.es/censos2021/C2021_Indicadores.csv` (also `.xlsx`),
  list of tables: `https://www.ine.es/censos2021/indicadores_seccen_c2021.xlsx`,
  boundaries (01/01/2021): `https://www.ine.es/censos2021/Cartografia_secc.zip`.
  Page: https://www.ine.es/uc/Kpj8DYAg (some section data flagged provisional).
- Logroño = `cpro 26`, `cmun 089`: **109 secciones**, 150,596 residents (655–2,684 per sección).
- 22 ready-made tables (t1–t22): population, sex, mean age, age in 3 broad groups (t4),
  foreign nationality, born abroad, studying, **higher education share (t9)**,
  **unemployment rate (t10)**, employed/active, **disability pensioners (t13)**, retirement
  pensioners, marital status, dwellings, tenure, households, **households by size (t22;
  t22_1 = single-person, all ages)**.
- Mapping to the paper's indicators (all proxies except where noted):
  | Paper | Census 2021 ready-made | Note |
  |---|---|---|
  | children < 10 (C) | t4_1 youngest broad group (check its age band; likely 0–15) | exact 0–9 needs padrón 5-year ages or INE custom table |
  | elderly singles 65+ (ES) | t22_1 single-person households (all ages) × t4_3 (65+) | "65+ living alone" needs custom table; 2011 Atlas de la Vulnerabilidad Urbana has "hogares unipersonales de mayores de 64" |
  | welfare recipients (WR) | t10 unemployment, t13 disability pensioners | better: INE ADRH share below 60 % of median income — per-sección availability **not yet confirmed** |
  | school leavers without diploma (EDQ) | 1 − t9 (no higher education) | different definition |
- INE ADRH (income atlas): https://ine.es/componentes_inebase/ADRH_total_nacional.htm ,
  methodology https://ine.es/metodologia/metodologia_adrh.pdf . The "distribution by income
  source" table may be municipal only (datos.gob.es lists "Municipios").

### Streets
Cadastre, IGN or OpenStreetMap (not yet checked).

## Recorded impacts (to turn into `data/impacts/logrono_events.csv`)

From local press (one row per place, with the source article; re-read each article
before recording — do not rely on this summary):

| Date | Reported | Source |
|---|---|---|
| 2018-09-17 | >30 incidents 18:42–19:30; calle Clavijo (driver rescued); LO-20 ring road; Portales | [nuevecuatrouno](https://nuevecuatrouno.com/2018/09/18/tormenta-en-logrono-inundacion-asegurada-en-la-circunvalacion/), [roads](https://nuevecuatrouno.com/2018/09/17/principales-carreteras-afectadas-por-la-tormenta-ap-68-y-lo-20/) |
| 2021-09-01 | ~10 streets; railway flooded; Logroño >½ of La Rioja Media's 112 calls | [nuevecuatrouno](https://nuevecuatrouno.com/2021/09/01/tormentas-rioja-incidencias-logrono-calahorra-navarrete/) |
| 2023-06-21 | >50 L/m² in about 1 h; calle Ebro, avenida Colón, calle Clavijo; garages flooded, car parks evacuated | [nuevecuatrouno](https://nuevecuatrouno.com/2023/06/21/tormenton-logrono-anega-ciudad-calles-garajes-parques-inundaciones/), [Infobae](https://www.infobae.com/espana/2023/06/22/inundaciones-en-logrono-las-tormentas-convierten-las-calles-de-la-ciudad-en-rios-de-barro/) |
| 2023-09 | council: critical points at raised pedestrian crossings without drainage | [nuevecuatrouno](https://nuevecuatrouno.com/2023/09/02/logrono-ayuntamiento-culpa-anterior-gobierno-inundaciones-tormentas/) |
| 2024-09 | SOS Rioja: 13 incidents in Logroño (one episode), 23 in another; premises, garages | [nuevecuatrouno](https://nuevecuatrouno.com/2024/09/22/mas-de-60-incidencias-en-toda-la-rioja-tras-la-tormenta/) |
| 2024-10-17 | ~30 incidents to the council; Paseo del Espolón, Club Deportivo roundabout, avenida Colón | [nuevecuatrouno](https://nuevecuatrouno.com/2024/10/17/noche-de-incidencias-manana-de-inundaciones-tormenton-en-logrono/) |

Other impact sources and their limits:
- SOS Rioja 112 / Ayuntamiento incident logs with addresses: only counts are public →
  data request (aggregated by street or sección for privacy); FAIR2Adapt could be a channel.
- Consorcio de Compensación de Seguros: flood claims per **municipality** only (viewer;
  ~50–60 % of damage insured) — too coarse for building level.
  [municipal analysis](https://consorsegurosdigital.com/almacen/pdf/analisis-de-los-danos-por-inundacion-en-espana-a-nivel-municipal.pdf)
- Event vs return period: REACHOUT events are 15-min; June 2023 is a ~1-h total. Matching
  an event to a map needs the 15-min intensity from the Logroño station.

## Suggested plan (follow CLAUDE.md phases)

- **Phase 1** — read the paper (already in the Hamburg repo: `paper/vogelbacher-2026.pdf`,
  CC BY); choose and verify the Quote for a replication claim (see decision 4); decide the
  chain shape with Anne.
- **Phase 2** — `01_data_download.py` (REACHOUT Logroño, Cadastre ATOM zip, INE indicators +
  boundaries, all checksummed with a source log); impacts CSV; `02_data_clean.py`
  (reproject REACHOUT to EPSG:25830, join building parts → floors, census → buildings,
  dwellings → residents).
- **Phase 3** — hazard, exposure, vulnerability, risk per building (reuse Hamburg scenario C
  code); impact comparison (do high-hazard buildings/streets coincide with recorded
  incidents more than random locations?); robustness to proxies and weights.
- Commit with the Claude co-author trailer (Anne's replication repos). Work in this repo,
  step by step, no subagents.

## Credits to carry over

Paper/method/data: Anastasia Vogelbacher, Malte von Szombathely, Marc Lennartz, Benjamin
Poschlod, Jana Sillmann. Hazard maps: Andrea Staccione, Jeremy S. Pal (REACHOUT).
Buildings: Dirección General del Catastro. Census: INE. Hamburg reproduction: Anne
Fouilloux.

## Follow-up

Climate-change and adaptation scenarios (REACHOUT CC/NBS, Destination Earth Climate DT
storylines and projections) are planned in a separate repository: see `FOLLOW-UP.md`.
