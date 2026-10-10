# 04 — FORRT Replication Study

> Run the pre-flight checklist in `docs/forrt-form-fields.md` § Pre-flight checklist before drafting.
>
> **Verify code first:** read the actual reproduction script in `notebooks/03_analysis.py` before writing the methodology field. See `docs/verify-before-drafting.md`.

## Field-by-field draft

<!-- field: study -->
### Short URI suffix for study ID (text input, required)

Slug. Use kebab-case.

```
logrono-pluvial-flood-replication-study
```

<!-- field: label -->
### Label/name of replication study (text input, required)

Human-readable title.

```
Replication in Logroño (Spain) with open data: building-level pluvial flood risk mapping tested against recorded flood impacts
```

<!-- field: type -->
### Choose the study type (dropdown, required)

- [x] Replication Study - replication with different methodology or conditions
- [ ] Reproduction/Replication Study - study that is both, reproduction and replication
- [ ] Reproduction Study - direct reproduction: same methodology, same tools

<!-- field: claim -->
### Choose FORRT claim (search/select, required)

URI of the Claim published in step 03. Pull from `nanopubs/PUBLISHED.md`.
Left empty here: the chain wizard carries the step-03 URI forward.

```

```

<!-- field: scope -->
### Describe what part of the claim is reproduced/replicated. (textarea, required)

The **scope** of the claim being tested. Which aspect, what's in/out of scope. NOT methodology. NOT results. See `docs/pico-study-outcome-levels.md`.

```
Whether building-level pluvial flood risk mapping, as proposed in the paper's framework, locates urban flood impacts more accurately than mapping at the scale of sub-city statistical units, when the framework is transferred to another city with open data only. In scope: the municipality of Logroño, Spain (6,315 buildings, 4,617 with residents; its 109 census sections as the sub-city units); the 100-year design storm, with return periods of 2 to 200 years as sensitivity; every index of the framework (social vulnerability, both exposures, both hazard indices, both risk indices and the risk classes) for every building; and, as the reference, the places where recorded storms caused flooding (13 distinct places from local press reports of six storms, 2018-2024). Testable against recorded impacts: the hazard component directly, the risk indices indirectly. Out of scope: validating social vulnerability (impact records do not say who was affected), the paper's own example and sensitivity analysis (reproduced in the Hamburg chain), other hazards, and future climate or adaptation scenarios (planned separately).
```

<!-- field: methodology -->
### Describe how the claim is reproduced/replicated. (textarea, required)

The **method** in plain prose. Read `notebooks/03_analysis.py` and any config files first. NOT exact numerical results.

```
A Snakemake pipeline (notebooks 01-04), open data only, from download to figures. Inputs: REACHOUT pluvial flood maps for Logroño (SaferRAIN, 2 m, baseline green cover; Zenodo 10.5281/zenodo.14035876); Spanish Cadastre INSPIRE buildings, building parts, cadastral zoning and addresses; INE Census 2021 indicators and section boundaries; Copernicus Urban Atlas 2018 (water, roads); OpenStreetMap features for reported places without an address. Preparation: flood extents at depth of at least 30, 40, ... 100 cm polygonised on the native grid and reprojected to ETRS89 / UTM 30N, water bodies removed; census population shared among buildings by Cadastre dwellings; ground-floor residents = residents / floors for residential buildings; census proxies for the four vulnerability indicators; street area = gaps between Cadastre urban blocks closed by 25 m, minus water. Risk: building-climate-risk v0.2.0 (10.5281/zenodo.23282971), the implementation that reproduces the authors' Hamburg example, with the paper's settings: TOPSIS with entropy (children 0.3 / elderly people living alone 0.7; welfare 0.5 / education 0.5; 0.5 / 0.5), flood-sensitivity threshold 0.25 x mean and exponent 2, hazard to well-being from a 2 m ring over depths 30-100 cm, hazard to mobility from 5 / 15 / 30 m rings at 30 cm, risk = social vulnerability x exposure x hazard, iterated-mean classes with three iterations. Robustness: alternative welfare proxy (disability pensioners), the sensitivity weights of the paper's text, no ground-floor residents in continuous urban fabric, Urban Atlas roads as street area, and vulnerability indicators as census-section rates instead of counts per building (with the rank correlation of the vulnerability index with building residents recorded for both). Impact test: each reported place, and every other street of the Cadastre address register as the baseline, gets the flooded share (at least 30 cm) of the open ground (not building, not water) within 20 m, the mean hazard to mobility and the highest mobility-risk class of buildings within 50 m; reported places are ranked among the baseline streets and their mean percentile is tested with a one-sided permutation test (10,000 shuffles, fixed seed), for subsets of places, a central-streets baseline and return periods of 2 to 200 years. Scale comparison: the same ranking with census-section values (flooded share of each section's open ground, overlap-weighted over each 20 m zone) instead of street-scale values, tested with a one-sided exact paired sign-flip test on the per-place percentile differences.
```

<!-- field: deviation -->
### Describe any deviations from original methodology. (textarea, optional)

What's different from the original method. Verify against the actual code, don't guess.

```
(1) Hazard model: REACHOUT SaferRAIN (hydrostatic fill-and-spill with Green-Ampt infiltration, no sewer network, 15-min design storm, 26.77 mm for the 100-year storm, 2 m grid in UTM zone 32) instead of the 2-D VISDOM model coupled with SWMM (60-min Euler-II storm of 36 mm, 1 m). Flood depths are not resampled; only the threshold polygons are reprojected. (2) Water bodies are removed from the flood extents: the rain-on-grid model also fills the river bed. (3) Population and social data: census sections shared among buildings by Cadastre dwellings; the paper's example used synthetic building-level data and did not disaggregate. (4) Census proxies for the indicators: children under 16 (not under 10); one-person households scaled by the share over 64 (elderly people living alone); unemployment (welfare recipients); residents without higher education (school leavers without diploma). (5) Ground-floor residents: the open Cadastre has no per-floor use, so residential buildings are assumed residential on the ground floor; buildings with dwellings but another main use get none (the paper's mixed-use rule). (6) Street area: gaps between Cadastre urban blocks, not road polygons. (7) Risk and classes over the buildings with residents; the authors' class rule is kept, so its means include the zero-risk buildings, a case the paper's example did not meet. (8) Method details inferred in the Hamburg reproduction are kept: sensitivity weights 0.3 / 0.7 (Eq. 2 and the authors' results; the text of Sect. 3.1.1 gives 0.7 / 0.3), TOPSIS vector normalisation, entropy in all three TOPSIS steps, three class iterations, rings that exclude every building footprint. (9) Open Python instead of ArcGIS Pro. (10) The comparison with recorded impacts and with census-section scale is an addition: the paper compares its scenario only qualitatively with two Hamburg events (Sect. 4.3.1).
```

<!-- field: keyword -->
### Search keywords (Wikidata) (search/select, optional)

Provide labels (not QIDs) — the Wikidata search picks up labels.

Each checked with `wikidata_lookup` (2026-10-10). Wikidata has no item for scientific
replication as such ("replication" returns DNA replication); reproducibility is used, as in
the Hamburg chain.

```
flood risk assessment (Q5460077)
urban flooding (Q15909735)
social vulnerability (Q581445)
open data (Q309901)
reproducibility (Q1425625)
```

<!-- field: discipline -->
### Search discipline (Wikidata) (search/select, optional)

Provide labels.

```
hydrology (Q42250)
```

## Publication note

After publishing, paste the resulting URI into `nanopubs/PUBLISHED.md` step 04.
