# Earnings Analysis Skill — Update Changelog

Session date: 2026-05-01

## Summary

Substantial expansion of the core earnings-analysis skill plus a new company-specific module for Carvana (CVNA) and a new guidance section in the AT&T module.

## SKILL.md (188 → 370 lines)

### Frontmatter
- Expanded `description` to surface what the skill produces (forward IOMA, balance sheet & cash flow YoY, share count tracking, company-module routing). Trigger phrases unchanged.

### Step 3 — Detailed sections (renumbered/expanded)
- **3e. Guidance** — replaced four-bullet stub with structured analysis:
  - Next-quarter guidance table with Low/High/Midpoint/Prior-Year-Same-Q Actual/Implied YoY%
  - Forward IOMA computation (next-quarter), with pessimistic/optimistic range and interpretation vs. trailing IOMA from 3c
  - Full-year guidance table with prior-quarter's-FY-guide-midpoint column for raise/lower/narrow/maintain detection
  - Forward FY IOMA
  - Qualitative read (direction, vs. consensus with beat-and-raise quality framing, tone, scenario caveats)
- **3f. Balance Sheet (YoY)** — new detailed YoY table covering: cash, ST/LT investments, AR, inventory, PP&E, AP, ST/LT/total/net debt. Per-bucket read guidance and strengthening/stable/weakening verdict.
- **3g. Cash Flow Statement (YoY)** — new section split into:
  - OCF and major drivers (NI, D&A, SBC, working capital, other) with one-time items watch and SBC-vs-D&A composition note
  - Capex and FCF — explicitly excludes financial-instrument purchases/sales; flags acquisitions and strategic investments separately
  - Capital allocation — buybacks, dividends, gross debt issuance/repayment, net debt issuance
  - **Diluted share count (YoY)** — trailing weighted-avg diluted/basic shares, down/flat/up read, cross-check against buyback dollar spend
  - **Forward share-count guide (if disclosed)** — current vs. FY-end guide with prior-quarter's-FY-guide column; covers the explicit-guide path and the EPS-and-net-income back-into path; reads for further reduction / flat / growth
- **3h. Management Commentary & Tone** — was 3g
- **3i. Stock Reaction Context** — was 3h

### Step 5 — Routing
- Added Carvana (CVNA) → `modules/cvna.md` to the company-specific modules table.

## modules/cvna.md (NEW — 496 lines)

New company-specific module for Carvana. Initially installed from uploaded source, then iteratively refined:

- **Carvana Context** — what CVNA is, segment structure, thesis backdrop
- **CVNA Thesis Tracker** (NEW, top-of-report executive summary):
  - Three-pillar thesis statement: (A) revenue growth + operating leverage, (B) earnings quality / no over-earning via inflated Other GPU, (C) long-term durability of 3M-units / 13.5% Adj EBITDA margin plan
  - Scorecard with 🟢 / 🟡 / 🔴 signals for each pillar
  - Per-pillar scoring rubric mapped to evidence in C1–C11 plus core skill sections
  - Composite read instruction and internal-consistency check vs. C11 bottom line
  - Valuation explicitly out of scope (handled separately later)
- **CVNA Dilution & Share-Count Notes** (orientation for filling out core 3g on CVNA):
  - "No company-issued share count guide" — instruction to mark forward FY share-count guide as `n/a — not guided`
  - Trailing dilution sources: SBC, senior secured PIK notes (debt-for-equity exchange watch), other convertibles/warrants, equity issuance
  - Class A vs. Class B mechanics (Garcia super-voting structure)
  - Practical instructions including regime-change triggers (buyback authorization or debt-for-equity exchange)
- **C1. Unit Economics Scorecard** (volume, GPU bridge, SG&A per unit, profitability)
- **C2. Reconditioning & Operational Efficiency**
- **C3. ADESA Integration Progress**
- **C4. Balance Sheet Strength / Weakness**
- **C5. Consumer Health & Demand Backdrop**
- **C6. Auto-Loan Origination, Sale, and ABS Performance**
- **C7. Liquidity Pipeline & Capital Partner Access**
- **C8. Headline Risk Watch** — durable description of related-party / DriveTime watch item (no longer references Gotham City Research January 2026 short report)
- **C9. Long-Term Plan Tracker**
- **C10. Miscellaneous — Topics Not Captured Above**
- **C11. Carvana-Specific Bottom Line**
- Source-attribution discipline at the end

## modules/att.md (93 → 127 lines)

- **NEW A7. AT&T Guidance Specifics** — pre-loaded checklist for filling out core 3e on AT&T:
  - Notes that AT&T is a full-year guider (no quarterly revenue/EPS guide)
  - Standard FY guide metrics table: Mobility service revenue growth, consolidated Adj EBITDA growth, Adj EPS, capital investment, FCF, net-debt-to-EBITDA leverage
  - Explicit warning that AT&T's "capital investment" includes vendor financing payments — not just cash capex
  - Less-consistent items watch list
  - Forward IOMA notes specific to AT&T (low-growth top line produces large/negative IOMA — interpret with magnitude caveat; prefer Adj EBITDA over Adj OI; FCF-based IOMA overlay)
  - Beat-and-raise pattern note: AT&T historically maintains rather than raises FY guidance; an actual raise is unusual and thesis-positive
- **A8. AT&T-Specific Bottom Line** — was A7

## Unchanged

- `modules/telecom.md` — no changes
- `modules/valuation.md` — no changes

## Suggested commit messages

If splitting into multiple commits:

```
feat(skill): add forward IOMA and structured guidance analysis (3e)
feat(skill): add detailed balance sheet YoY analysis (3f)
feat(skill): add cash flow YoY analysis with share count tracking (3g)
feat(skill): add forward FY share-count guide block
chore(skill): renumber 3g/3h to 3h/3i; update output format reference
feat(modules): add CVNA company module with thesis tracker
feat(modules/att): add A7 AT&T guidance specifics
chore(skill): expand frontmatter description to reflect expanded scope
```

If single commit:

```
Expand earnings-analysis skill: forward IOMA, BS/CF YoY, share count tracking, CVNA module

- Add structured guidance section (3e) with forward IOMA on next-quarter and FY guides
- Add detailed balance sheet YoY analysis (3f) covering cash, investments, AR/AP, PP&E, inventory, debt structure, net debt
- Add cash flow statement YoY analysis (3g) with OCF driver decomposition, capex (excluding financial instruments), capital allocation, and diluted share count tracking with forward FY guide
- Renumber 3g/3h to 3h/3i; update output format reference
- Add CVNA company-specific module with three-pillar thesis tracker, dilution & share-count notes, and structural sections C1–C11
- Add A7 AT&T Guidance Specifics with capital-investment-vs-capex warning and AT&T-specific forward IOMA calibration
- Expand frontmatter description to surface new capabilities; trigger phrases unchanged
```
