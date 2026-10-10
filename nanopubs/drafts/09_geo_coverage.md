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

Left blank: resolved by the form's location search for "Hamburg, Germany".

```

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
