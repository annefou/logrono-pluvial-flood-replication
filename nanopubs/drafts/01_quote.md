# 01 — Quote-with-comment (paper-rooted chains)

> Run the pre-flight checklist in `docs/forrt-form-fields.md` § Pre-flight checklist before drafting.
>
> If this is a question-rooted chain, use `01_pico.md` or `01_pcc.md` instead — see `docs/chain-decision-tree.md`.
>
> **After choosing the chain shape, delete the two step-1 alternates you aren't using.** Once you've decided this chain is paper-rooted and keep `01_quote.md`, run:
> ```bash
> rm nanopubs/drafts/01_pico.md nanopubs/drafts/01_pcc.md
> ```

**Form heading:** *"Annotate a paper quotation — Annotating a paper quotation with personal interpretation"*

## Field-by-field draft

<!-- field: paper -->
### Cited DOI (text input, required)

Format: starts with `10.` — bare DOI, **NOT** `https://doi.org/...` form.

```
10.5194/nhess-26-2765-2026
```

### Quote mode (radio button)

- [x] **Quote whole text (less than 500 characters)**
- [ ] Quote start/end *(use this if the quote exceeds 500 chars)*

<!-- field: quotation -->
### The exact quotation from the paper (max. 500 characters) (textarea, required)

Verbatim from `paper/vogelbacher-2026.pdf`, p. 15 (Sect. 6, Conclusions and outlook).
`verify_quote` → found, match `normalized` (whitespace / line-break hyphenation only),
pdf sha256 `88121b0e…a7d5`.

```
This finer level of granularity has the potential to significantly enhance the accuracy of urban risk assessments and support decision-making regarding disaster risk management and climate adaptation.
```

Character count: 200 / 500.

<!-- field: quotation-end -->
### End of quotation (optional - use when quoting beginning and end of a longer passage, max. 500 characters) (textarea, optional)

Only when quoting the beginning *and* end of a longer passage — set the mode above to
**Quote start/end**, put the opening phrase under the previous heading and the closing
phrase here. Leave empty for a single short quote.

```

```

<!-- field: comment -->
### Our interpretation and explanation of why this quotation is relevant (max. 800 characters) (textarea, required)

Standalone interpretation (true independently of this replication); live form caps at 500 chars.

```
The authors present building-level resolution as a route to more accurate urban flood risk assessment, but the paper gives no quantitative check against observed flooding: Sect. 4.3.1 only compares the design storm qualitatively with two Hamburg events, and the worked example uses synthetic building data. The accuracy gain is therefore stated as a potential; it can be tested wherever flood impacts have been recorded.
```

Character count: 420 / 500.

## Publication note

After publishing, paste the resulting URI into `nanopubs/PUBLISHED.md` step 01.
