# 10 — Proposal: geographic coverage of a replication's own study area

Not a draft of an existing template: a **proposal** for a Science Live template, written
2026-10-10 because the existing "Document geographical coverage" template cannot express
this replication's study area honestly (see `09_geo_coverage.md`).

## The gap

"Document geographical coverage" anchors coverage to **a paper DOI + a verbatim quotation
from that paper**. That fits the original paper's area (Hamburg for Vogelbacher et al. 2026).
A replication that transfers a method to a new place — here Logroño, Spain — has no paper
sentence naming *its* area, so it cannot be published without misattributing the area to the
original paper. The same gap applies to any transfer study (e.g. a Sado-Estuary method tested
on the Westerschelde).

## Proposed template: "Document the study area of a replication study"

| Field | Kind | Notes |
|---|---|---|
| Replication Study | guided choice, required | the FORRT Replication Study nanopub whose area this is (subject of the coverage) |
| Short ID for location | text, required | slug, e.g. `logrono` |
| Area name | text, required | e.g. `Logroño, La Rioja, Spain` |
| Geometry (WKT) | map / text, required | from the location search or drawn — or derived from a cited boundary dataset (next field); never hand-written |
| Geometry source | external URI, optional | the boundary dataset the geometry comes from |
| Role of the area | choice, optional | e.g. *study area*, *analysis extent*, *validation sites* |
| Comment | textarea, required | how the area relates to the study (scope, what was analysed there) |

Same GeoSPARQL `wktLiteral` as the existing template, so spatial search and the story-page
map work unchanged; only the subject (a Study nanopub instead of a paper + quote) differs.

## Values for this replication (once the template exists)

- **Replication Study**: the step-04 URI of this chain.
- **Location**: `logrono` — **Area name**: `Logroño, La Rioja, Spain` (municipality, INE code 26089).
- **Geometry**: the municipal boundary as the union of its 109 census sections — **Geometry
  source**: INE, Censos 2021, section boundaries (01/01/2021),
  https://www.ine.es/censos2021/Cartografia_secc.zip (downloaded and checksummed by
  `notebooks/01_data_download.py`). Alternatively the form's geocoder for the area name.
- **Role**: study area. The analysis extent is the urban area (Cadastre blocks closed by 25 m),
  and the validation sites are the 13 reported flood places (`data/impacts/`).
- **Comment**: the building-level pluvial flood risk framework of Vogelbacher et al. (2026)
  transferred to Logroño with open data, and its flood hazard compared with flooding recorded
  in local press (2018–2024).

Until the template exists, the area is recorded as spatial coverage in the repository
metadata (RO-Crate / codemeta) at release time.
