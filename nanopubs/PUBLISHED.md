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

| Location | URI | Published | Status |
|---|---|---|---|
| Hamburg, Germany (paper's area) | https://w3id.org/sciencelive/np/RAXrw7VYNnaHeaIrX4hJsOCJ7Aqy17nbt77LRzP9WOQWc | 2026-10-10 | **To be replaced**: geometry is the location search's bounding box (10,300 km², includes the Wadden Sea exclave and Lower Saxony); republish with the WKT in `nanopubs/drafts/09_geo_coverage.md`, then retract this one with the CLI (needs the signing key) |
