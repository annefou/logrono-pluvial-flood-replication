# 02 — AIDA Sentence

> Run the pre-flight checklist in `docs/forrt-form-fields.md` § Pre-flight checklist before drafting.

**Form heading:** *"AIDA Sentence — Make structured scientific claims following the AIDA model"*

## Field-by-field draft

<!-- field: aida -->
### AIDA sentence (text input, required)

Atomic, Independent, Declarative, Absolute. One empirical finding. Must end with a full stop.

> _If your draft AIDA contains "and" linking two distinct findings, split into two AIDA nanopubs._

Atomicity check: one finding — a comparison of accuracy between two spatial scales.
Derived from the Quote (Sect. 6: "This finer level of granularity has the potential to
significantly enhance the accuracy of urban risk assessments", with "shifting the spatial
scale from sub-city units to individual buildings" in the same paragraph); stated without
the hedge, as AIDA requires. Deliberately carries no city, dataset or number (as in the
Hamburg chain), so another city can test the same statement. Logroño, the census sections
as sub-city units and the recorded impacts live in the Study and the Outcome.
Length: 142 / 500.

```
Building-level pluvial flood risk mapping locates urban flood impacts more accurately than mapping at the scale of sub-city statistical units.
```

<!-- field: topic -->
### Select related topics/tags (search/select, optional)

Predefined topic vocabulary — list the labels you intend to pick from the dropdown.

Each checked with `wikidata_lookup` (2026-10-10). Wikidata has no item for "pluvial
flooding" itself (only articles about it). Logroño is a place, not a topic class;
its coverage belongs in step 09.

| Label | QID | type (P31/P279) |
|---|---|---|
| urban flooding | Q15909735 | flood |
| flood risk | Q2288778 | disaster risk |
| flood risk assessment | Q5460077 | field of study; risk assessment |

```
urban flooding (Q15909735)
flood risk (Q2288778)
flood risk assessment (Q5460077)
```

<!-- field: project -->
### Relates to this nanopublication (search/select, required)

URI of the nanopub the AIDA derives from.

- For paper-rooted chains: the Quote-with-comment URI (from step 01).
- For question-rooted chains: the PICO or PCC URI (from step 01).

Pull the URI from `nanopubs/PUBLISHED.md`.
Left empty here: the chain wizard carries the step-01 URI forward.

```

```

<!-- field: dataset -->
### Supported by datasets (text input, optional)

DOIs/URLs of datasets that ground the AIDA claim.

The open flood maps the finding rests on (REACHOUT, Staccione and Pal 2024, CC BY 4.0;
cited by the paper itself in Sect. 4.3.2 as a basis for transfer). One URL per bullet line —
`build-chain-draft` reads this field from bullets only.

- https://doi.org/10.5281/zenodo.14035876

<!-- field: publication -->
### Supported by other publications (text input, optional)

DOIs/URLs of publications that support the AIDA claim — e.g. peer-reviewed methods papers, or the original paper if not already cited via the Quote.

*(skip — optional)* The paper is already cited through the Quote (step 01). Leaving this
empty also avoids the known bug below when both "supported by" fields are filled.

> **Known platform bug (2026-04-26):** if both *Supported by datasets* AND *Supported by other publications* are populated and publishing fails, fall back to publishing this AIDA via Nanodash. The URI namespace becomes `https://w3id.org/np/...` (still valid and citable).

## Publication note

After publishing, paste the resulting URI into `nanopubs/PUBLISHED.md` step 02.
