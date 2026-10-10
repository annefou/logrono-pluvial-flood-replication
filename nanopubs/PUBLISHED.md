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

The original paper's study area (subject: doi:10.5194/nhess-26-2765-2026), published with the
"Document geographical coverage" template.

| Location | URI | Published | Status |
|---|---|---|---|
| Hamburg, Germany (mainland; WKT from OSM relation 62782 via `scripts/geo_coverage_wkt.py`, 745.2 km²) | https://w3id.org/sciencelive/np/RA1NTaGnBgz1AFkx-Xbpl8FLq16t6wINM-XyP4PrsXnK8 | 2026-10-10 | **current** — checked: content matches the draft, WKT identical to `nanopubs/geo/hamburg.wkt` |
| Hamburg, Germany (first attempt) | https://w3id.org/sciencelive/np/RAXrw7VYNnaHeaIrX4hJsOCJ7Aqy17nbt77LRzP9WOQWc | 2026-10-10 | **superseded, retraction pending** — geometry is the location search's bounding box (10,300 km², incl. the Wadden Sea exclave); retracting needs the original signing key, not available outside Science Live |
