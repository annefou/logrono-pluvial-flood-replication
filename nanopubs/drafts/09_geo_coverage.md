# 09 — Geographical coverage (optional)

> Run the pre-flight checklist in `docs/forrt-form-fields.md` § Pre-flight checklist before drafting. Read `docs/geo-coverage.md` first.
>
> **When to draft this.** Only when the paper's findings have a **specific geographic
> scope** — a study area, region, country, transect, or named site (typical for
> earth-observation, biodiversity, ecology, epidemiology work). A non-spatial paper
> (e.g. a lab cognition study with no study area) has **no** geographic coverage —
> delete this draft and skip the step. Do not invent a location to fill the form.
>
> **What it documents.** The geographic coverage of the **original paper** (subject =
> the paper DOI), backed by a **verbatim quotation** from the paper that names the
> area. Grounded, Record-side — place name and quote from the PDF; geometry resolved
> by the form's map/geocoder, never hand-written. Publishes with the platform's
> existing **"Document geographical coverage"** template; discoverable via GeoSPARQL.

## More than one location

A paper can cover **several areas**. Handle it one of two ways:

- **Distinct study sites** (separately meaningful — e.g. two estuaries compared, three
  field sites): publish **one coverage nanopub per site**, so each is individually
  named, quoted, and spatially searchable. Duplicate the *per-location block* below,
  once per site — each with its **own** area name, **own** verbatim quote, and own
  geometry. This is the atomic default.
- **One pooled coverage** (regions the study treats as a single combined extent —
  e.g. "North America, the EU and Australia" pooled in one analysis): publish **one**
  nanopub. In the form's location search, add each place in turn — it merges them into
  a single `GEOMETRYCOLLECTION` under one combined label. Use one block below, list
  the places in the label, and quote the sentence that names them together.

If unsure, prefer separate nanopubs — atomic coverage is easier to search and cite.

## Shared field

<!-- field: paper -->
### Cited DOI (text input, required — same for every location)

The **original paper's** DOI (bare, starting `10.` — the form prepends `https://doi.org/`). Same DOI as the Quote (step 01) / CiTO (step 06). Read it from `CITATION.cff` `references:`; do not recall it.

```
10.5194/nhess-26-2765-2026
```

---

## Per-location block — duplicate this whole section once per distinct site

> Publish one "Document geographical coverage" nanopub per block below. For a single
> location, keep one block. For a pooled multi-region coverage, keep one block and add
> each place in the form's location search (it builds the GeometryCollection).

### Location A — Hamburg, Germany (the original paper's study area)

**Paper (shared `paper` field above):** `10.5194/nhess-26-2765-2026` — Vogelbacher et al. (2026),
*A high-resolution framework for urban pluvial flood risk mapping*, NHESS 26, 2765–2783.

`verify_quote` (2026-10-10): found, p. 1 (Abstract), match `normalized`, pdf sha256 `88121b0e…a7d5`.
The paper does not name the city quarter of its worked example ("a city quarter in Hamburg",
"a single statistical unit (neighbourhood) in Hamburg"), so the coverage is the city as the
paper frames it — no narrower geometry is invented.

<!-- field: quoteType -->
**Quote type** (radio: whole | ends, required) — `whole` if under 500 characters (usual); `ends` only for a long start/end passage.

```
whole
```

<!-- field: quotation -->
**Quoted Text** (textarea, required) — the **verbatim** sentence from the paper naming *this* area. Character-for-character from the PDF; never paraphrase. Each location needs its own quote.

```
The framework is demonstrated using empirical data from Hamburg, Germany, identifying risk hotspots where high social vulnerability coincides with elevated flood exposure.
```

<!-- field: quotation-end -->
**Quoted Text End** (textarea, optional — only if quote type = ends). Leave blank for `whole`.

```

```

<!-- field: location -->
**Short ID for location** (text input, required) — slug for the URI suffix (lowercase, hyphenated), unique per location. E.g. `sado-estuary`, `westerschelde`, `amazon-basin`.

```
hamburg
```

<!-- field: location-label -->
**Area name** (text input, required) — human-readable name as the paper frames it. E.g. `Sado Estuary, Portugal`. Typing this into the form's **location search** geocodes it and fills the geometry.

```
Hamburg, Germany
```

<!-- field: geometry -->
**Short ID for geometry** (text input, optional) — URI suffix for the geometry node; `coverage` is fine.

```
coverage
```

<!-- field: wkt -->
**Geometry as Well-known Text (WKT)** (map / text, resolved in the form) — **Do NOT hand-write coordinates.** The form geocodes the area name to a polygon, or you draw it on the map. Only paste explicit `POINT(...)` / `POLYGON((...))` if the paper **states coordinates verbatim** — copied exactly. A hallucinated bounding box is a fabricated datum; leave blank otherwise.

**Paste this WKT** — do not use the form's location search: it stores the area's bounding
box, which for Hamburg spans its Wadden Sea exclave at the Elbe mouth (published once that way
on 2026-10-10: a 10,300 km² rectangle, of which Hamburg is 9.5 %).

Generated by `scripts/geo_coverage_wkt.py hamburg 62782 --utm 32632` from OpenStreetMap
relation 62782 (ODbL): mainland part only (the exclave dropped, holes dropped), simplified
at 400 m so it fits the template's 1,500-character cap — 88 vertices, 1,448 characters,
745.2 km² (−0.24 % vs the full-detail mainland). Provenance: `nanopubs/geo/hamburg.json`.

```
POLYGON ((9.7301 53.5576, 9.7744 53.5543, 9.7656 53.5411, 9.7813 53.5186, 9.7711 53.5219, 9.7636 53.5083, 9.7846 53.5, 9.782 53.4923, 9.8028 53.4938, 9.7998 53.4694, 9.8618 53.4296, 9.8622 53.44, 9.8987 53.458, 9.9172 53.4466, 9.9229 53.4364, 9.9108 53.4141, 9.9421 53.421, 9.9438 53.4295, 9.9759 53.4219, 9.9765 53.4138, 9.9833 53.4146, 9.9959 53.4259, 10.0292 53.4353, 10.0146 53.442, 10.0222 53.4476, 10.0454 53.4464, 10.042 53.4566, 10.0516 53.4639, 10.085 53.4508, 10.1079 53.4271, 10.1368 53.4221, 10.1761 53.3966, 10.2374 53.3961, 10.2597 53.4183, 10.3178 53.4353, 10.3253 53.4498, 10.3123 53.4522, 10.3097 53.4431, 10.2993 53.4435, 10.299 53.4507, 10.2693 53.4641, 10.2644 53.4751, 10.2385 53.4825, 10.2369 53.4963, 10.2183 53.4992, 10.2239 53.5056, 10.2104 53.5199, 10.1878 53.5115, 10.1624 53.5225, 10.1688 53.5374, 10.1519 53.5355, 10.1484 53.546, 10.1605 53.561, 10.1478 53.5642, 10.1525 53.5779, 10.1619 53.5858, 10.2013 53.584, 10.1889 53.6131, 10.222 53.6336, 10.1896 53.6384, 10.1959 53.6548, 10.14 53.6804, 10.1589 53.6903, 10.1569 53.7045, 10.1723 53.7124, 10.1816 53.7089, 10.1917 53.7227, 10.1937 53.731, 10.1677 53.7393, 10.1211 53.7132, 10.082 53.7204, 10.0692 53.7109, 10.0775 53.6994, 10.0604 53.6883, 10.0693 53.6795, 9.9996 53.6815, 9.9858 53.6482, 9.921 53.6555, 9.9069 53.6525, 9.8892 53.6229, 9.8248 53.5842, 9.7913 53.6013, 9.7963 53.6103, 9.7705 53.616, 9.7713 53.6314, 9.7345 53.5826, 9.7425 53.578, 9.7301 53.5576))
```

<!-- field: comment -->
**Comment** (textarea, required) — one or two sentences on **how the quoted text supports** this being the coverage. Grounded in the paper, no new claims.

```
The abstract states that the framework is demonstrated with empirical data from Hamburg, Germany. The worked example is a building-level realisation informed by one statistical unit (a city quarter) in Hamburg, which the paper does not name; the coverage is therefore the city.
```

### Logroño (the replication's own study area) — not drafted here

This template documents the *paper's* coverage (paper DOI + a verbatim quote naming the
area). The paper does not study Logroño — it only lists it among cities with REACHOUT flood
maps (Sect. 4.3.2) — so a Logroño coverage nanopub would misstate the paper's scope. It
needs a template whose subject is the Replication Study; proposed in
`nanopubs/drafts/10_replication_area_proposal.md`.

## Publication note

Each location block is a **standalone** nanopub, not one of the six FORRT chain steps.
Publish each via the platform's **"Document geographical coverage"** template (Create →
that template). After publishing, paste each resulting URI into `nanopubs/PUBLISHED.md`
under a "Geographical coverage" row (one row per location) so `/verify-chain` and the
story page can find them.
