# Paper summary

> This is a working scratchpad for the paper-analysis phase. The output of this file feeds the Quote / AIDA / Claim drafts. It is not itself a nanopub.

**Reference paper:** A high-resolution framework for urban pluvial flood risk mapping

**DOI:** 10.5194/nhess-26-2765-2026

**Authors:** Anastasia Vogelbacher, Malte von Szombathely, Marc Lennartz, Benjamin Poschlod, Jana Sillmann

**Year:** 2026 (Nat. Hazards Earth Syst. Sci., 26, 2765–2783)

**PDF:** `paper/vogelbacher-2026.pdf` (CC BY 4.0), sha256 `88121b0ee6a93e9b79bf5386bd46496900f6dc4cdd88e9009e7af89660d0a7d5`

## Headline claim

Chosen with Anne on 2026-10-10. The quote is from p. 15, Sect. 6, and `verify_quote` found it (`normalized` match):

> This finer level of granularity has the potential to significantly enhance the accuracy of urban risk assessments and support decision-making regarding disaster risk management and climate adaptation.

Other candidates that also passed `verify_quote` but were not chosen:

- p. 1, Abstract: "The transparent and flexible design makes the framework transferable to other cities, supporting climate adaptation planning and risk-informed decision-making."
- p. 14, Sect. 5: "By providing the toolbox along with its input data structure and code, we enable its transferability and adaptability to other regions, including those with coarser data, as demonstrated in this work."
- p. 15, Sect. 6: "The framework and toolbox, developed in close collaboration with city stakeholders through co-creation processes, enables such downscaling and provides a transferable structure that can be applied to other cities as well."

## Methodology summary

- **Data sources:** The paper uses one Hamburg statistical unit (a city quarter) with **synthetic** building-level data. Social and exposure values are distributed to buildings by expert judgement so that they reproduce the unit's aggregate values (Sect. 2.1). The paper includes a disaggregation tool but states that this study does not use it. Hazard comes from the HAMBURG WASSER pluvial simulation: a 100-year design rainfall of 36 mm in 60 min (Euler-II), modelled with 2-D VISDOM coupled bidirectionally with SWMM (the sewer network), on a 1 m DTM (Sect. 2.4). Streets and building use come from ALKIS.
- **Model:** risk = social vulnerability × exposure × hazard, following the IPCC framework (Sect. 3).
  - *Social vulnerability:* TOPSIS combined with Shannon entropy. Sensitivity uses children under 10 and elderly people over 65 living alone; coping capacity uses welfare recipients and school leavers without a diploma. A flood-sensitivity transformation is then applied.
  - *Exposure:* residents per building, or residents on the ground floor for well-being.
  - *Hazard:* the flooded fraction of rings around each building for depths of 30–100 cm, passed through a log-normal CDF. Mobility also uses the street area within 0–15 m and 15–30 m.
  - *Output:* two indices, risk to well-being (PFR_WB) and risk to mobility and accessibility (PFR_MA), each classified into relative classes by iterated means.
- **Sample size:** 37 buildings and one rainfall scenario.
- **Headline numbers:** none against observations. Sect. 4.3 is a sensitivity analysis. Sect. 4.3.1 compares the scenario only qualitatively with the Lohbrügge (2018-05-10) and Barmbek (2024-06-02) events. The Hamburg reproduction (prior chain, Validated) matched the authors' risk classes for 37/37 buildings.

## Replication design choice

- [ ] **Reproduction Study** — direct reproduction: same methodology, same tools.
- [x] **Replication Study** — replication with different methodology or conditions.
- [ ] **Reproduction/Replication Study** — both.

This is a new city (Logroño, Spain) with new open data, so it is a Replication Study:

- **Hazard:** REACHOUT SaferRAIN maps (Staccione and Pal, 2024, doi:10.5281/zenodo.14035876; the paper cites them in Sect. 4.3.2). SaferRAIN is a hydrostatic model with infiltration and no sewer network, on a 2 m grid with 15-min design storms; RP100 is 26.77 mm.
- **Buildings:** Spanish Cadastre INSPIRE data.
- **Vulnerability:** INE Census 2021 indicators per sección censal, used as proxies and disaggregated to buildings.
- **Method:** the Hamburg scenario C implementation is reused.

The chain **extends** the Hamburg reproduction chain (CiTO entry `RAI00BYT…`).

## Notes for downstream drafts

- **Chain shape (decided with Anne, 2026-10-10):** one paper-rooted chain. The comparison with recorded flood impacts (local press, 2018–2024; `data/impacts/logrono_events.csv`) is the main evidence in the Outcome.
- **The AIDA must be about accuracy against observed impacts, not "risk highest where E and H coincide".** The latter is true by construction of risk = SV × E × H.
- **Recorded impacts test hazard and exposure only, not social vulnerability.** Say so in the Study scope and in the Outcome limitations.
- The quote is hedged ("has the potential"). The claim type and Outcome wording must not overstate what the paper asserts.
- **Inferred method details carried over from Hamburg.** Sensitivity weights are children 0.3 / elderly singles 0.7; TOPSIS uses vector normalisation; entropy is applied in all three steps; the classes use three iterations; hazard rings exclude all building footprints.
- **Geographic coverage (09):** the original paper's study area is a Hamburg city quarter. Check whether the Hamburg repo already published it before drafting it here.
