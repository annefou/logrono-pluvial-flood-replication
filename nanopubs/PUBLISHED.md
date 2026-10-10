# Published nanopub chain — URI registry

This file is the canonical registry of published nanopub URIs for this replication. Update it as you publish each step.

## Chain

| Step | Template | URI | Published |
|---|---|---|---|
| 01 | Quote-with-comment (or PICO / PCC) | _not yet published_ | |
| 02 | AIDA Sentence | _not yet published_ | |
| 03 | FORRT Claim | _not yet published_ | |
| 04 | FORRT Replication Study | _not yet published_ | |
| 05 | FORRT Replication Outcome | _not yet published_ | |
| 06 | CiTO Citation | _not yet published_ | |

## Optional layers

| Step | Template | URI | Published |
|---|---|---|---|
| 07 | Research Software (if applicable) | _not applicable / not yet published_ | |
| 08 | Research Synthesis (if applicable) | _not applicable / not yet published_ | |

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
