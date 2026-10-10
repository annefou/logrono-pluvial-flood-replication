# 05 — FORRT Replication Outcome

> Run the pre-flight checklist in `docs/forrt-form-fields.md` § Pre-flight checklist before drafting.
>
> **Verify the actual numerical results first** by reading `results/` and `notebooks/03_analysis.py`. Don't quote numbers from memory. See `docs/verify-before-drafting.md`.

## Field-by-field draft

<!-- field: outcome -->
### Short URI suffix for outcome ID (text input, required)

Slug. Use kebab-case.

```
logrono-pluvial-flood-outcome
```

<!-- field: label -->
### Plain-text label for the outcome (text input, required)

Descriptive title.

```
Building-level pluvial flood risk transferred to Logroño with open data: modelled flooding matches recorded impacts, risk indices only weakly (partially supported)
```

<!-- field: study -->
### Choose study (search/select, required)

URI of the Replication Study published in step 04. Pull from `nanopubs/PUBLISHED.md`.

```
«URI of step 04 — FORRT Replication Study (filled by the chain wizard)»
```

<!-- field: repo -->
### Repository URL (text input, required)

Use the Zenodo **version DOI** URL for the release the results came from — not a
bare branch URL, and not the concept DOI.

> **Why not the bare repo URL.** `https://github.com/ORG/REPO` names a *moving
> branch*. This Outcome asserts "this code produced this number", in a signed,
> immutable record. A branch URL means that assertion points at whatever `main`
> happens to be years from now — code that may never have produced the number
> above. A concept DOI has the same flaw: it resolves to the latest version.
> The version DOI pins the exact release. `docs/chain-decision-tree.md` § Anchor
> ranks the options: SWHID > Zenodo DOI > repo URL > Wayback.
>
> Both DOIs and the SWHID are in `CITATION.cff` under `identifiers:`, recorded
> automatically at release by `.github/workflows/release-identifiers.yml`. Take
> the one described as *"Version DOI"*.

```
https://doi.org/{{ZENODO_VERSION_DOI}}
```

<!-- field: date -->
### Choose completion date (text input, required)

```
2026-10-10
```

<!-- field: validationStatus -->
### Choose validation status (dropdown, required)


This dropdown maps to the CiTO intention in step 06: Validated → `confirms`, PartiallySupported → `qualifies`, Contradicted → `disputes`.

- [ ] contradicted
- [ ] inconclusive
- [ ] not tested
- [x] partially supported
- [ ] validated

<!-- field: confidenceLevel -->
### Choose confidence level (dropdown, required)

```
moderate
```

- [ ] high - Strong evidence, mostly agrees with original
- [ ] low - Limited evidence, significant disagreement
- [x] moderate - Adequate evidence, partial agreement
- [ ] very high - Extensive evidence, high agreement with original
- [ ] very low - Minimal evidence, major disagreement

<!-- field: conclusion -->
### Describe the overall conclusion about the original claim (textarea, required)

Substantive interpretation. Headline comparison: replication's number vs the paper's number, sign + significance.

```
Partially supported. The paper states that building-level granularity "has the potential to significantly enhance the accuracy of urban risk assessments". Transferred to Logroño (Spain) with open data only, the framework's hazard component is accurate where it can be checked: places where recorded storms (2018-2024) caused flooding are among the most flooded places in the open 2 m flood map (REACHOUT), far more than other streets, for every design storm. This supports the claim for the part of a risk assessment that says where water causes problems.

The claim as a whole, about risk assessments, could only be partly tested. Risk = social vulnerability x exposure x hazard, and recorded impacts (press reports of flooded streets, underpasses, garages, a hospital car park) say where water caused trouble, not who was affected or how vulnerable they were. Social vulnerability was therefore not tested, and exposure only indirectly. The building-level risk indices agree only weakly with the recorded places; this is expected by design (several reported places are roads and underpasses with no residents beside them, where the framework correctly gives high hazard but low risk to residents) and is not evidence against them. The accuracy of the building-level risk classes themselves remains unvalidated.
```

<!-- field: evidence -->
### Describe the evidence that supports your conclusion (textarea, required)

Numerical results, test statistics, model coefficients. Read directly from `results/`.

```
Test: for each of 13 distinct places reported flooded in local press (6 storms, 2018-2024; 14 reports), the share of open ground within 20 m flooded at least 30 cm in the 100-year design storm, ranked among 512 other Logroño streets (Cadastre address register); one-sided permutation test of the mean percentile, 10,000 shuffles (p = 0.0001 is the smallest attainable).

Hazard (what impacts can test): reported places rank at the 83.8th percentile on average vs all streets (p <= 0.0001) and the 88.6th vs the 143 streets in continuous urban fabric (p <= 0.0001); 12 of 13 places are above the median street, while 57.8 % of streets have no modelled flooding at all. Like-for-like subset (6 places located by Cadastre addresses, as the baseline): 78.3th percentile (p = 0.0064), 82.5th vs central streets (p = 0.0022). Press-only and without-approximate-locations subsets give 82.6th-88.9th percentiles (all p <= 0.0001). Across design storms of 2 to 200 years the mean percentile stays between 83.4th and 89.5th (all p <= 0.0001). Strongest matches: calle Clavijo underpass under the N-111 and calle San Gregorio (99.2th percentile each); the one miss is Paseo del Espolón (no modelled flooding, 28.9th percentile).

Risk (vulnerability x exposure x hazard): mean hazard to mobility of buildings within 50 m ranks at the 63.6th-68.1th percentile (p = 0.028-0.085 across subsets and baselines); the highest mobility-risk class within 50 m at the 60.8th-65.9th (p = 0.018-0.156). Example: the Clavijo underpass (99.2th percentile for flooding) has only no-risk residential buildings within 50 m.

Risk mapping: building-climate-risk v0.2.0 (10.5281/zenodo.23282971; reproduces the authors' Hamburg example, 37/37 classes) on 4,617 residential buildings (150,596 residents); authors' iterated-mean classes: risk to well-being 5 buildings high or very high (1,105 residents), risk to mobility 10 (2,002 residents). Hotspots are stable to the welfare proxy, the sensitivity weights and the street source (70-100 % retained), not to the ground-floor assumption (well-being: 1 of 5 retained, Spearman 0.683).
```

<!-- field: limitations -->
### Describe what limits the conclusions of the study (textarea, optional)

Honest caveats. If the result is partial or contradicted, say so plainly. Don't overclaim.

```
What could not be tested: (1) social vulnerability - impact reports do not record who was affected; testing it needs impact data on people, e.g. emergency calls or evacuations by address and household (SOS Rioja 112 / Logroño council logs, available only on request and aggregated); (2) exposure, only indirectly; (3) therefore the accuracy of the building-level risk classes, the core output of the framework.

Impact data: 13 distinct places from press reports, a small sample with low power for the risk measures; press attention favours busy central places (a stricter central-streets baseline gives the same result); one place comes from a post embedded in an article, two locations are approximate; several places are roads or an underpass located with OpenStreetMap, while the baseline streets are located by Cadastre addresses (the like-for-like subset of 6 street places still differs from the baseline). Storms are matched to design storms only loosely: REACHOUT storms last 15 min, the reported events 15-60 min with different totals; the result holds for every return period from 2 to 200 years.

Transfer choices that differ from the paper: hazard from REACHOUT SaferRAIN (hydrostatic fill-and-spill with infiltration, no sewer network, 2 m grid in UTM zone 32, 26.77 mm in 15 min for the 100-year storm) instead of the paper's VISDOM-SWMM model (36 mm in 60 min, 1 m); water bodies removed from the flood extents (the rain-on-grid model also fills the Ebro's bed); census-section proxies for the paper's indicators (children under 16 instead of under 10; one-person households x share over 64 for elderly people living alone; unemployment for welfare recipients; no higher education for school leavers without diploma), shared among buildings by Cadastre dwellings; ground-floor residents = residents / floors for residential buildings (no per-floor use in the open Cadastre; the well-being hotspots depend strongly on this); street area = gaps between Cadastre urban blocks. Method details inferred in the Hamburg reproduction (sensitivity weights 0.3 / 0.7, TOPSIS vector normalisation, entropy in all three steps, three class iterations) are kept. The authors' class rule averages over all buildings, including the 85-92 % with zero risk here; their 37-building example did not face this choice.
```

## Publication note

After publishing, paste the resulting URI into `nanopubs/PUBLISHED.md` step 05.
