---
name: telecom-provider-analysis
description: >
  Use this skill whenever the user provides earnings documents (press release, supplemental
  materials, earnings call transcript, investor slides) for a single US telecom service provider
  and wants a structured operational snapshot of the company at that point in time. Covers the Big 3
  wireless carriers (AT&T / T, Verizon / VZ, T-Mobile / TMUS) and the major cable connectivity
  providers (Comcast / CMCSA / Xfinity, Charter / CHTR / Spectrum). Triggers include uploading any
  earnings doc from these companies and phrases like "analyze [provider]'s quarter", "what did
  [provider] report", "snapshot of [provider]", "how was the quarter". Use this skill ALWAYS when
  earnings docs from one of the five providers are uploaded, even with casual phrasing. Output
  includes general telecom KPIs and company-specific idiosyncratic metrics. For multi-company
  comparisons or industry-wide analysis, use the sibling skill `industry-competitive-positions`.
---

# Telecom Provider Analysis Skill

A single-company workflow for extracting and structuring the operational performance of US telecom service providers from their earnings documents. Designed to produce a comprehensive snapshot of the company **at this point in time** — which becomes one input to later industry-wide competitive analysis (handled by the sibling skill `industry-competitive-positions`).

## Scope

This skill covers five providers:

| Company | Ticker | Profile Type | Universal Module | Company Module |
|---|---|---|---|---|
| AT&T | T | Wireless-led + fiber | `modules/wireless-led.md` | `companies/att.md` |
| Verizon | VZ | Wireless-led + fiber + FWA | `modules/wireless-led.md` | `companies/verizon.md` |
| T-Mobile | TMUS | Wireless pure-play + FWA | `modules/wireless-led.md` | `companies/tmobile.md` |
| Comcast | CMCSA | Cable connectivity + content | `modules/cable-led.md` | `companies/comcast.md` |
| Charter | CHTR | Pure-play cable connectivity | `modules/cable-led.md` | `companies/charter.md` |

Anything outside these five providers is out of scope — fall back to the general `earnings-analysis` skill.

## Inputs

The user typically provides one or more of:
1. **Press release** — official results document; primary source for headline financials
2. **Supplemental investor materials / financial trends** — segment KPI detail, often the richest source for wireless/broadband subscriber metrics
3. **Earnings slides / investor presentation** — visual segment data, guidance, narrative
4. **Earnings call transcript** — prepared remarks + Q&A; primary source for management tone, forward commentary, and color on outliers

If only some inputs are provided, proceed and note what's missing. If a key metric isn't disclosed in the documents available, write "not disclosed" rather than guessing.

---

## Workflow

### Step 1 — Identify the Provider

From document content, ticker, branding, or user mention, identify which of the five providers the docs are from. If the document is from a provider not in the five, stop and tell the user this skill doesn't cover that provider; redirect to general `earnings-analysis`.

### Step 2 — Load the Universal Module

Load the appropriate sub-industry module:
- **Wireless-led** (AT&T, Verizon, T-Mobile) → `modules/wireless-led.md`
- **Cable-led** (Comcast, Charter) → `modules/cable-led.md`

This module specifies the **universal telecom KPIs** to extract — metrics that apply to any provider in that sub-industry.

### Step 3 — Load the Company Module

Load `companies/<provider>.md`. This file contains **idiosyncratic** content only:
- Segment structure quirks unique to that company
- Company-specific named programs and assets (e.g., FirstNet, Frontier acquisition, NBCU, RDOF buildouts)
- Stated strategic thesis
- Watch-list items unique to that company
- Recent corporate actions / pending deals

There is **no overlap** between the universal module and the company module by design. The universal module covers what's common; the company module covers what's distinctive.

### Step 4 — Extract Metrics

Working through the documents:
- Pull the universal KPIs specified in Step 2's module
- Pull the idiosyncratic items specified in Step 3's company module
- Always tag the period (Q3 2025, FY 2024, etc.) and currency
- Where management cites a driver for a result, capture it concisely (5–10 words) — never invent drivers not in the docs

### Step 5 — Produce the Single-Company Output

The output has four parts, in this order:

#### Part A — Header & Company Context (compact)

```
[Company] ([Ticker]) — Q[X] [YYYY] Operational Snapshot
─────────────────────────────────────────────────────────
Period reported: [exact period]
Reporting basis:  [GAAP, adjusted, etc.]
Strategic posture (this quarter): [1-line — pulled from company module's stated thesis, refined by what the docs emphasize]
```

#### Part B — Snapshot Card (universal metrics)

A compact, scannable card laying out the universal KPIs from the sub-industry module. Same shape every time, so any single-company snapshot is later usable as input to the industry-competitive-positions skill.

```
┌─ WIRELESS / MOBILE ────────────────┬─ BROADBAND / FIXED ───────────────┐
│ Postpaid phone net adds:    [X]    │ Total broadband net adds:   [X]   │
│ Postpaid phone churn:       [X%]   │ Fiber/HFC subs:             [X]   │
│ Postpaid phone ARPU:        [$X]   │ Broadband ARPU:             [$X]  │
│ Wireless service rev growth: [+X%] │ Fiber/FWA footprint:        [X]   │
│ EBITDA service margin:      [X%]   │ Convergence/bundle attach:  [X%]  │
├─ FINANCIAL ────────────────────────┴───────────────────────────────────┤
│ Revenue: $[X] (YoY [+/-X%])  |  EBITDA margin: [X%]  |  FCF: $[X]      │
│ Capex: $[X] (intensity [X%])  |  Net debt / EBITDA: [X.Xx]             │
│ Capital return (div + bb): $[X]                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

For cable providers, fields substitute per `modules/cable-led.md` (mobile lines instead of postpaid phone, etc.). Mark genuinely inapplicable fields "n/a"; mark undisclosed fields "not disclosed".

#### Part C — Detail Sections (universal)

Follow the section order specified by the universal module (wireless-led has 10 sections; cable-led has 9). Be analytical, not just descriptive — explain what the numbers mean, not just what they are. Keep each section tight; the snapshot is a working artifact, not an essay.

#### Part D — Company-Specific Section (idiosyncratic)

Append a clearly labeled **"Company-Specific Update"** section that covers idiosyncratic items from the company module:
- Progress on company-specific named programs (e.g., AT&T's 30M fiber passings target, Verizon-Frontier integration, T-Mobile's Magenta MAX mix, Comcast's Versant spinoff, Charter's RDOF buildout)
- Segment-structure-specific commentary (e.g., AT&T's Business Wireline decline pace, Comcast's Connectivity & Platforms isolation from NBCU)
- Recent corporate actions, pending deals, and idiosyncratic balance-sheet items
- Anything the company itself emphasizes that isn't a universal KPI

#### Part E — Where They Stand (3 bullets)

Three bullets that map this quarter's results to the company's stated three-part thesis (the company module specifies what the three thesis pillars are for each provider). Each bullet says: thesis pillar → progress this quarter → directional read.

### Step 6 — Save the Snapshot as a PDF

After producing the chat output, save a PDF copy via the **`analysis-snapshot-pdf`** skill so the analysis is durable across sessions. **Mandatory by default** — only skip if the user explicitly says "chat only" or "don't save."

`analysis-snapshot-pdf` owns all formatting concerns (typography, layout, fonts, page setup). This step only specifies the telecom-specific bits: where the file goes, what it's named, and how to map the snapshot content into that skill's block schema.

**File location:**
- Prefer the company-specific subfolder inside the user's workspace folder (e.g., `…/VZ/`, `…/Charter/`, `…/CMCSA/`, `…/T/`, `…/TMUS/`). Match the existing folder name used for the source documents.
- If no such subfolder exists, save into the workspace root and tell the user where it landed.
- Do not silently overwrite an existing file for the same period — append a version suffix (e.g., `… Snapshot v2.pdf`) or ask the user.

**Filename convention:** `<TICKER> Q<X> <YYYY> Snapshot.pdf` — e.g., `VZ Q1 2026 Snapshot.pdf`, `CHTR Q4 2025 Snapshot.pdf`.

**Content payload (mapping to the `analysis-snapshot-pdf` schema):**

- `title`: `<Company Name> (<Ticker>) — Q<X> <YYYY> Operational Snapshot`
- `subtitle`: `Reported <date> · Quarter ended <date>`
- `metadata`: three rows — Period reported / Reporting basis / Strategic posture (one-line)
- `blocks`:
    1. `card` block titled "Snapshot Card", with groups taken from the universal-module card mapping (wireless-led: WIRELESS / MOBILE, BROADBAND / FIXED, FINANCIAL — or the cable-led equivalents)
    2. `sections` block titled "Detail" with `label_style: heading`, items keyed `W1.` … `W10.` (wireless-led) or `C1.` … `C8.` (cable-led), bodies as paragraphs
    3. `sections` block titled "Company-Specific Update" with `label_style: inline`, items being the idiosyncratic-module bullets
    4. `numbered` block titled "Where They Stand" with the three thesis pillars
- `footer_id`: `<Ticker> Q<X> <YYYY> Operational Snapshot`
- `sources`: list of input filenames actually used (press release, transcript, supplements, etc.)

Construct the dict, write to a temp JSON file, and run `analysis-snapshot-pdf`'s renderer against it (or import the renderer directly). Then surface a `computer://` link to the saved PDF in the reply.

Remember: in any string body, escape literal `&` `<` `>` as `&amp;` `&lt;` `&gt;`, but keep `<b>` / `<i>` / `<sub>` / `<super>` tags as XHTML for inline emphasis.

---

## Output Format Rules

- Lead with Part A (Header & Context), then Part B (Snapshot Card), then Part C (universal detail), then Part D (company-specific), then Part E (Where They Stand)
- Use tables where data is comparative across periods or segments
- Keep prose tight — this skill produces a working snapshot, not a research note
- Always state the period covered
- If a metric is undisclosed, write "not disclosed" — do not estimate from indirect data unless explicitly requested
- For non-USD reporting (e.g., AT&T Mexico in pesos), state currency and any FX caveat
- Always finish by saving the snapshot as a PDF per Step 6 (unless the user opts out) and surface the file link

---

## Notes & Discipline

- **Do not invent drivers.** When stating why a metric moved, paraphrase what management said — if management didn't say, write "driver not disclosed".
- **Do not over-describe well-disclosed numbers.** If postpaid net adds were +400K, just say so — don't pad with three sentences of context.
- **Multi-company comparison and industry-view requests** belong in the `industry-competitive-positions` skill, not here. If the user uploads multiple providers' docs and asks for comparison or industry view, recommend they invoke that skill — though completing single-company snapshots first is fine and is the natural input to that workflow.
- **Cable wireless reporting is structurally different** from Big 3 wireless reporting. The cable-led module handles this — don't try to force Big 3 metrics onto Comcast/Charter.
- **For Comcast specifically**, isolate Connectivity & Platforms from Content & Experiences (NBCU, Peacock, parks). The connectivity snapshot is the focus; non-connectivity is one paragraph in the company-specific section, no more.
- The output of this skill is designed to be **picked up later** by the `industry-competitive-positions` skill once snapshots from 2+ providers in the same period are available.
