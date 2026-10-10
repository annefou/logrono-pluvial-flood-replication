# 06 — CiTO Citation

> Run the pre-flight checklist in `docs/forrt-form-fields.md` § Pre-flight checklist before drafting.

**Description:** *"Declare citations between papers or other works, using Citation Typing Ontology"*

## Field-by-field draft

<!-- field: work -->
### Identifier for the citing creative work (text input, required)

URI of the Outcome published in step 05. Pull from `nanopubs/PUBLISHED.md`.
Left empty here: the chain wizard carries the step-05 URI forward.

```

```

### List citations (repeatable group, required ≥1)

#### Citation 1 — back to the original paper

##### Citation Type (dropdown)

Choose based on the Outcome's validation status:

- Validated → `confirms`
- PartiallySupported → `qualifies`
- Contradicted → `disputes`

Outcome: partially supported → **qualifies**.

For question-rooted chains where there is no original paper to confirm/dispute, use `usesMethodIn` or `citesAsAuthority` for the methodology paper(s).

Write the chosen type in the block below (a vocabulary label such as `cites as authority`, or `citesAsAuthority`). `build-chain-draft` uses it as written; leave the block empty to have the type derived from the Outcome's validation status, which is right for paper-rooted chains only.

> **Note:** `replicates` is NOT in the Science Live dropdown (despite existing in upstream CiTO). When citing a notebook/tutorial that was directly reused, use **`credits`** instead.

```
qualifies
```

##### DOI or other URL of the cited work (text input)

```
https://doi.org/10.5194/nhess-26-2765-2026
```

#### Additional citations (optional)

If the Outcome cites methods papers, related replications, or upstream tools, add them here.

One line per further citation, in this exact form (each becomes a pre-filled row):

- Type: extends → URL: https://w3id.org/sciencelive/np/RA6V_jAy2OFjYBwQMOH92fIM6199bjez7hRkY90vkxx7U
- Type: usesDataFrom → URL: https://doi.org/10.5281/zenodo.14035876
- Type: citesAsDataSource → URL: https://doi.org/10.2909/9911fe21-57f6-46fb-ae26-d76e7bb6378f
- Type: citesAsDataSource → URL: https://www.catastro.hacienda.gob.es/INSPIRE/buildings/ES.SDGC.BU.atom.xml
- Type: citesAsDataSource → URL: https://www.ine.es/censos2021/C2021_Indicadores.csv
- Type: credits → URL: https://doi.org/10.5281/zenodo.23282971

  (extends: the Hamburg chain's Outcome — the validated reproduction of the authors' example
  that this replication builds on; `CITATION.cff` lists the chain's apex. usesDataFrom: the
  REACHOUT flood maps. citesAsDataSource: Urban Atlas 2018, the Cadastre INSPIRE feed, the INE
  Census 2021 indicators. credits: building-climate-risk v0.2.0, the implementation used. All
  checked 2026-10-10: the w3id, Urban Atlas, Cadastre and INE URLs return 200; the two Zenodo
  DOIs resolve (`resolve_doi`; Zenodo refuses HEAD requests).)

## Publication note

After publishing, paste the resulting URI into `nanopubs/PUBLISHED.md` step 06.

This completes the six-step FORRT chain. Optional next layers:

- **Research Software** (`drafts/07_research_software.md`) — if the repo *produces* a reusable software artefact.
- **Research Synthesis** (`drafts/08_synthesis.md`) — if this chain is one of several testing facets of a shared property.
