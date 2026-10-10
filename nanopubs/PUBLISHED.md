# Published nanopub chain — URI registry

This file is the canonical registry of published nanopub URIs for this replication. Update it as you publish each step.

## Chain

| Step | Template | URI | Published |
|---|---|---|---|
| 01 | Quote-with-comment | https://w3id.org/sciencelive/np/RAbgREdIegl6pbTP_E4E2Eg9JR28whinZDteeGueXg1Wc | 2026-10-10 |
| 02 | AIDA Sentence | https://w3id.org/sciencelive/np/RAPjP2vEln1AzhH3QpkUK6lRB99xicwcRkdUp35bxk9U4 | 2026-10-10 |
| 03 | FORRT Claim | https://w3id.org/sciencelive/np/RAQDtKtTjDH3tbUuBwmzk2mWYe7vyMKHMI1cquwB-Pltk | 2026-10-10 |
| 04 | FORRT Replication Study | https://w3id.org/sciencelive/np/RABBJpiR9zQUaRlSclmmv5wvIJr8wWl_hyo-NBK2o10pI | 2026-10-10 |
| 05 | FORRT Replication Outcome | https://w3id.org/sciencelive/np/RAzO2FoYqdwvPCDDkfVmf-SKOl2mUpsf_qZeje0i_LP_U | 2026-10-10 |
| 06 | CiTO Citation | https://w3id.org/sciencelive/np/RAoFYugT7OVk5eoHuxKCO9HeqA08jMfSn7TeUxwZcbezE | 2026-10-10 |

**Chain shape:** paper-rooted — Quote-with-comment → AIDA → FORRT Claim → Replication Study →
Replication Outcome → CiTO Citation. Published 2026-10-10 through the Science Live chain wizard,
from `nanopubs/chain-draft.json` at commit 3eca53a (built from release v0.1.1).

**Outcome:** `partially supported`, confidence `moderate`; repository = release v0.1.1
(https://doi.org/10.5281/zenodo.23285198). The CiTO relation to the original paper is `qualifies`;
it `extends` the Hamburg reproduction chain (Outcome
https://w3id.org/sciencelive/np/RA6V_jAy2OFjYBwQMOH92fIM6199bjez7hRkY90vkxx7U).

Full URIs, for copy-paste:

```
01 quote    https://w3id.org/sciencelive/np/RAbgREdIegl6pbTP_E4E2Eg9JR28whinZDteeGueXg1Wc
02 aida     https://w3id.org/sciencelive/np/RAPjP2vEln1AzhH3QpkUK6lRB99xicwcRkdUp35bxk9U4
03 claim    https://w3id.org/sciencelive/np/RAQDtKtTjDH3tbUuBwmzk2mWYe7vyMKHMI1cquwB-Pltk
04 study    https://w3id.org/sciencelive/np/RABBJpiR9zQUaRlSclmmv5wvIJr8wWl_hyo-NBK2o10pI
05 outcome  https://w3id.org/sciencelive/np/RAzO2FoYqdwvPCDDkfVmf-SKOl2mUpsf_qZeje0i_LP_U
06 citation https://w3id.org/sciencelive/np/RAoFYugT7OVk5eoHuxKCO9HeqA08jMfSn7TeUxwZcbezE
```

## Verification (2026-10-10)

`verify_chain` (forrt-research-mcp 0.1.2) against the **dev** API (`api-dev.sciencelive4all.org`; the
production `/np/constellation` endpoint returned HTTP 500 to the tool at the time): **green — 11 pass, 0 fail**.
All six steps enumerated in the constellation; the Outcome's repository resolves (release v0.1.1,
10.5281/zenodo.23285198); cited targets resolve (the paper, building-climate-risk v0.2.0, the Hamburg Outcome).

**Correction to one row.** The tool's `verdict-relation` row read "verdict Validated matches CiTO
confirms" — that is the *Hamburg* chain's pair, reached through this chain's `extends` citation of the
Hamburg Outcome. Read from the published TriG, this chain's Outcome is **PartiallySupported**
(confidence Moderate) and its CiTO cites the paper with **qualifies** — the pair the tool's own rule
requires. The CiTO carries all seven citations of the draft (qualifies, extends, usesDataFrom,
citesAsDataSource ×3, credits).

## Optional layers

| Step | Template | URI | Published |
|---|---|---|---|
| 07 | Research Software (if applicable) | _not applicable here_ — the reusable tool is `building-climate-risk` (its own repository) | |
| 08 | Research Synthesis (if applicable) | _not yet published_ — candidate: Hamburg reproduction + Logroño replication of the same paper | |

## Format

URIs from Science Live are of the form `https://w3id.org/sciencelive/np/RA…`. URIs from Nanodash (used as a fallback when the Science Live UI hits a bug) are of the form `https://w3id.org/np/RA…`. Both are valid and citable.

If a URI is not in the Science Live namespace, view it via the Science Live viewer by wrapping the URI:

```
https://platform.sciencelive4all.org/np/?uri=<full-URI>
```

## Cross-references

- Drafts: `nanopubs/drafts/`
- Form structure: `docs/forrt-form-fields.md`
- Chain shape decision: `docs/chain-decision-tree.md`

## Geographical coverage (standalone, not a chain step)

Published with the "Document geographical coverage" template: the original paper's study area
(subject: doi:10.5194/nhess-26-2765-2026) and this replication's own (subject: its v0.1.0 release).

| Location | URI | Published | Status |
|---|---|---|---|
| Hamburg, Germany (mainland; WKT from OSM relation 62782 via `scripts/geo_coverage_wkt.py`, 745.2 km²) | https://w3id.org/sciencelive/np/RA1NTaGnBgz1AFkx-Xbpl8FLq16t6wINM-XyP4PrsXnK8 | 2026-10-10 | **current** — checked: content matches the draft, WKT identical to `nanopubs/geo/hamburg.wkt` |
| Logroño, La Rioja, Spain (this replication's study area; cited work = release v0.1.0, 10.5281/zenodo.23284601; WKT from OSM relation 340516, 78.9 km²) | https://w3id.org/sciencelive/np/RAzds1z9t2ac7XFvx_Hsv18__p5nUTNA0NHIsskSyLVPQ | 2026-10-10 | **current** — checked: DOI, quote (verbatim in the Zenodo description) and comment match the draft, WKT identical to `nanopubs/geo/logrono.wkt`; short ID `city`, label "Logroño" |
| Hamburg, Germany (first attempt) | https://w3id.org/sciencelive/np/RAXrw7VYNnaHeaIrX4hJsOCJ7Aqy17nbt77LRzP9WOQWc | 2026-10-10 | **superseded; disapproved by the author** (https://w3id.org/np/RA6ME0ZiWgCCxdZTHq6qZoO3PsemLCJ1_g7p_vsNJqysw, Nanodash, 2026-10-10: "The area for Hamburg is far too large and it is misleading.") — geometry is the location search's bounding box (10,300 km², incl. the Wadden Sea exclave); a retraction would need the original signing key |
