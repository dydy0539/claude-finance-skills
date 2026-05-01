---
name: earnings-analysis
description: >
  Use this skill whenever the user wants to analyze a company's earnings results.
  Triggers include: uploading or referencing a press release, earnings slides, or transcript;
  phrases like "analyze this earnings", "break down the quarter", "what did [company] report",
  "run earnings analysis", or "earnings call summary". Also trigger when the user shares
  multiple earnings documents together and asks for any kind of synthesis or commentary.
  Always use this skill even if the request seems simple — e.g. "what were the highlights"
  or "how was the quarter" — as long as an earnings document is involved.
  The skill produces a structured report covering revenue, profitability, trailing and
  forward IOMA, segment breakdown, guidance with YoY % change and forward IOMA, detailed
  YoY balance sheet and cash flow analysis, diluted share count tracking with forward FY
  share-count guide, management commentary, and stock reaction. Routes to company-specific
  modules (AT&T, Carvana) when the company matches, which add thesis trackers, idiosyncratic
  metrics, and tailored guidance handling.
---

# Earnings Analysis Skill

A structured workflow for analyzing a company's quarterly or annual earnings from primary source documents.

## Inputs

The user will typically provide one or more of the following (in order of priority):
1. **Press release** — The official results document (PDF or text). Primary source for financials.
2. **Earnings slides / investor presentation** — Supplemental visuals; check for segment detail, guidance tables, and KPIs not in the press release.
3. **Earnings transcript** — CEO/CFO prepared remarks + analyst Q&A. Primary source for tone, forward commentary, and qualitative color.

If only some inputs are provided, proceed with what's available and note what's missing.

---

## Workflow

### Step 1 — Company Context (assume zero prior knowledge)

Before diving into numbers, briefly orient the reader:
- What does the company do? (1–2 sentences, plain English)
- What segment(s) or business lines matter most?
- What are the 2–3 key metrics the market watches for this company?

If the documents don't provide enough context, use your own knowledge or note the gap.

---

### Step 2 — Scorecard (brief, at the top)

Produce a concise scorecard table summarizing the quarter at a glance:

| Metric | Result | YoY Δ% | Key Driver (from docs) | Signal |
|--------|--------|---------|------------------------|--------|
| Revenue | $X | +Y% | e.g. "strength in X segment, mgmt cited Y" | 🟢 / 🟡 / 🔴 |
| Adj. Operating Income / EBITDA | $X | +Y% | e.g. "margin expansion from cost actions" | 🟢 / 🟡 / 🔴 |
| IOMA | X% | — | e.g. "operating leverage on fixed cost base" | 🟢 / 🟡 / 🔴 |
| Gross Margin | X% | +Y bps | e.g. "favorable product mix" | 🟢 / 🟡 / 🔴 |
| Guidance (next Q / FY) | $X–$Y | Raised / Lowered / In-line | e.g. "raised on macro tailwinds" | 🟢 / 🟡 / 🔴 |
| Stock Reaction | +X% / -X% | — | e.g. "beat offset by soft guidance" | context only |

**Rules for the Key Driver column:**
- Pull directly from the press release, slides, or transcript — quote the reason management gave, paraphrased concisely (5–10 words)
- If no reason is stated in the documents, write "not disclosed"
- Never invent or infer a driver not mentioned in the source documents
- If multiple drivers are cited, list the primary one; add a secondary in brackets if meaningful

Signal key: 🟢 Beat / positive, 🟡 In-line / mixed, 🔴 Miss / negative

---

### Step 3 — Detailed Sections

Cover each section below in order. Use headers. Be analytical, not just descriptive — explain what the numbers mean, not just what they are.

#### 3a. Revenue & Growth
- Total revenue and YoY growth rate
- Organic vs. reported growth if disclosed
- Geographic or end-market breakdown if available
- Any notable acceleration or deceleration vs. recent trend

#### 3b. Profitability
- Gross margin (and YoY change)
- Operating income (GAAP and/or adjusted) and margin
- Adjusted EBITDA if disclosed
- Note any one-time items, restructuring charges, or SBC that distort comparisons

#### 3c. IOMA — Incremental Operating Margin Analysis
Apply Yi's IOMA framework:

**IOMA = ΔAdjusted Operating Income (YoY) ÷ ΔRevenue (YoY)**

- Use **non-GAAP / adjusted operating income** by default
- Compare **year-over-year** (same quarter, prior year) — not sequential
- Express as a percentage
- Interpret: >50% = strong operating leverage; 20–50% = healthy; <20% = limited leverage or investment mode; negative = margin contraction despite growth

If the user says "use GAAP instead", "run IOMA on guidance", or "do FY vs FY", apply that variant accordingly.

#### 3d. Segment Breakdown
- Revenue and growth by segment (table format if 3+ segments)
- Which segment drove the beat or miss?
- Any inflection points — a segment turning profitable, a new product line ramping, etc.

#### 3e. Guidance

If management provides forward guidance, capture it in a structured comparison vs. the **prior-year same-period actual** (which the user will provide if not directly available in the source documents). This enables YoY growth computation on each guided line and a **forward IOMA** to surface what operating leverage management is implying.

##### Next-quarter guidance

| Metric | Guide Low | Guide High | Midpoint | Prior-Year Same-Q Actual | Implied YoY Δ% (Midpoint) |
|---|---|---|---|---|---|
| Revenue | | | | | |
| Adjusted operating income | | | | | |
| Adjusted EBITDA | | | | | |
| Adjusted EPS | | | | | |

If only a point estimate is given (no range), fill Midpoint and leave Low / High blank. If guidance is given as a YoY growth % rather than absolute dollars, derive the implied dollar level from the prior-year actual and note the derivation.

**Additional guided items to capture as extra rows whenever management discloses them:**

- Capex
- Free cash flow
- Gross margin (%)
- Operating margin (% or bps change)
- Effective tax rate
- Diluted share count (cross-reference to the forward share-count block in 3g)
- Segment-level revenue or operating income (one row per segment)
- Volume / unit metrics (subscribers, units sold, customers, etc.)
- Currency / FX assumptions if material

##### Forward IOMA (next-quarter)

Apply Yi's IOMA framework to next-quarter guidance:

**Forward IOMA = (Guided Adj OI midpoint − Prior-Year Same-Q Adj OI) ÷ (Guided Revenue midpoint − Prior-Year Same-Q Revenue)**

Use **Adj OI** by default. If only Adj EBITDA is guided (no Adj OI), use Adj EBITDA and label accordingly. If both are guided, compute both versions.

Also compute the implied **range**, since guidance is usually a range:
- **Pessimistic IOMA** = (Guide-Low Adj OI − Prior-Year Adj OI) ÷ (Guide-Low Revenue − Prior-Year Revenue)
- **Optimistic IOMA** = (Guide-High Adj OI − Prior-Year Adj OI) ÷ (Guide-High Revenue − Prior-Year Revenue)

**Interpret vs. trailing IOMA from Step 3c:**

- **Forward IOMA > Trailing IOMA** = management implying margin tailwind / operating leverage acceleration; bullish read.
- **Forward IOMA ≈ Trailing IOMA** = continuation of current margin trajectory.
- **Forward IOMA < Trailing IOMA** = implying margin pressure, an investment cycle, or reinvestment of operating upside; flag whether management explained the step-down.
- **Negative Forward IOMA** = guiding to margin contraction even with revenue growth → significant tonal shift; flag prominently.

If guidance lacks the data needed (e.g., Adj OI not guided, or revenue is the only guided line), note "forward IOMA not computable — [reason]" rather than fabricating an estimate.

##### Full-year guidance (if disclosed)

If management gives FY guidance, build a parallel table including a column for the **prior quarter's FY guide midpoint** so you can immediately see whether FY guidance was raised, lowered, narrowed, or maintained this quarter.

| Metric | FY Guide Low | FY Guide High | Midpoint | Prior FY Actual | Implied YoY Δ% (Midpoint) | Prior Quarter's FY Guide Midpoint | Δ vs. Prior Guide |
|---|---|---|---|---|---|---|---|
| Revenue | | | | | | | |
| Adjusted operating income | | | | | | | |
| Adjusted EBITDA | | | | | | | |
| Adjusted EPS | | | | | | | |
| Capex | | | | | | | |
| Free cash flow | | | | | | | |

Compute **Forward FY IOMA** = (Guided FY Adj OI midpoint − Prior FY Adj OI) ÷ (Guided FY Revenue midpoint − Prior FY Revenue), interpreted the same way as the next-quarter version.

##### Qualitative read

- **Direction:** raised, lowered, narrowed, or maintained vs. the prior quarter's guide? (Headline read; cross-reference the prior-guide column.)
- **Vs. consensus:** if consensus estimates are available or mentioned in source materials, note where guidance midpoints land vs. consensus. **Beat-and-raise quality:** if the company beats by $X but only raises FY by $Y where Y < X, that's a conservative reset; raising by ≥ the beat signals genuine acceleration; raising by less than half the beat is a yellow flag worth calling out.
- **Tone:** confident, cautious, or non-committal? Watch for hedging language ("expect to see," "anticipate," "depending on macro," "subject to," "if conditions persist") vs. confident language ("will achieve," "raising our outlook," "we are committed to," "have line of sight").
- **Scenario / sensitivity caveats:** FX assumptions, segment-specific risks, macro contingencies, regulatory dependencies, or one-time tailwinds the guide explicitly bakes in.

#### 3f. Balance Sheet (YoY)

Compare each line item to the **same quarter in the prior year** (not sequential — most balance sheet items are seasonal). Pull from the 10-Q balance sheet or earnings supplemental tables. If a line item is not disclosed or not material for the company, mark "n/a" rather than leaving blank.

| Item | This Quarter | Prior-Year Quarter | YoY Δ$ | YoY Δ% | Read |
|---|---|---|---|---|---|
| Cash & cash equivalents | | | | | |
| Short-term investments | | | | | |
| Long-term investments | | | | | |
| Accounts receivable | | | | | |
| Inventory | | | | | |
| Property, plant & equipment (net) | | | | | |
| Accounts payable | | | | | |
| Short-term debt (incl. current portion of LT debt) | | | | | |
| Long-term debt | | | | | |
| Total debt | | | | | |
| Net debt (total debt − cash − ST investments) | | | | | |

**Read guidance:**
- **Liquidity (cash + ST/LT investments):** Building YoY alongside flat/declining debt = strengthening; drawdown alongside flat debt = weakening unless explained by capex or working-capital build for growth.
- **Receivables:** Growing materially faster than revenue = collection slippage or longer-dated customer mix; flag.
- **Inventory:** Growing faster than revenue = potential demand softness or sourcing front-run; flag and look for management explanation. Growing slower than revenue = healthy turn acceleration.
- **PP&E:** Track YoY change against capex run-rate to spot capacity additions, divestitures, or impairments.
- **Payables:** Growing faster than COGS = working-capital tailwind / supplier-stretch; growing slower = drag.
- **Net debt:** The headline read for deleveraging progress. YoY decline = strengthening; rise = weakening unless tied to a refinancing that lowers cash interest cost or accretive M&A — flag the trade in either case.

In 1–2 sentences, score the balance sheet as **strengthening / stable / weakening** YoY based on the combined read.

#### 3g. Cash Flow Statement (YoY)

Compare same-period vs. prior year (quarter or YTD — note which). The goal is to (a) decompose the YoY change in operating cash flow, (b) isolate one-time items, (c) separate real capex from financial-instrument flows, and (d) lay out capital allocation.

##### Operating cash flow and major drivers

| Item | This Period | Prior-Year Period | YoY Δ$ |
|---|---|---|---|
| **Cash flow from operations** | | | |
| ↳ Net income | | | |
| ↳ Depreciation & amortization (add-back) | | | |
| ↳ Stock-based compensation (add-back) | | | |
| ↳ Working capital changes (net) | | | |
| ↳ Other material non-cash items | | | |

After the table, in 2–4 sentences, identify the **2–3 largest drivers** of the YoY change in operating cash flow. Common drivers: working-capital swings (inventory build/release, AR collections, AP stretch), deferred-revenue moves, tax payments/refunds, and one-time settlements.

**One-time items watch:** Flag any large discrete cash items that distort the YoY comparison — litigation settlements, restructuring cash payments, large tax payments or refunds, asset-sale gains/losses (cash portion), or insurance recoveries. Quantify if disclosed.

**Add-back composition note:** SBC and D&A both flow through OCF as add-backs but represent very different things — SBC is real economic cost being excluded from cash measurement, D&A is non-cash by nature. Track YoY direction of each:
- **SBC growing faster than revenue** = increasing dilution per dollar of growth; flag in conjunction with share-count change.
- **D&A growth** = capex catch-up or recent acquisition amortization; cross-check against PP&E and intangibles balances in 3f.

##### Capex and free cash flow

| Item | This Period | Prior-Year Period | YoY Δ$ |
|---|---|---|---|
| Capex — purchases of PP&E | | | |
| Capitalized software / capitalized R&D (if disclosed) | | | |
| **Total operating capex** | | | |
| **Free cash flow (OCF − total operating capex)** | | | |
| FCF margin (FCF / revenue) | | | |

**Important exclusions from capex:** Purchases and sales of marketable securities, short-term investments, treasury bills, and other financial instruments are NOT capex — they represent treasury management, not capacity investment. Strip them out before computing FCF even though they sit in the investing section.

Also exclude from "capex" but flag separately if material:
- **Acquisitions** (cash, net of cash acquired)
- **Strategic investments / equity stakes**

##### Capital allocation (financing activities)

| Item | This Period | Prior-Year Period | YoY Δ$ |
|---|---|---|---|
| Share repurchases | | | |
| Dividends paid | | | |
| Debt issuance (gross proceeds) | | | |
| Debt repayment / redemption | | | |
| **Net debt issuance / (repayment)** | | | |

Commentary to add:
- **Buyback program** — new authorization, pace acceleration, or pause? Compare quarterly buyback run-rate to authorization size remaining.
- **Dividend** — raise, cut, special dividend, or initiation?
- **Refinancing trades** — new issuance paired with redemption: note the rate / maturity trade.
- **Equity issuance** (ATM, follow-on, convert) — flag if any, with size and use of proceeds.

##### Diluted share count (YoY)

The net effect of buybacks vs. SBC and any other issuance shows up here. Pull weighted-average share counts from the income statement (same period vs prior-year same period).

| Item | This Period | Prior-Year Period | YoY Δ | YoY Δ% |
|---|---|---|---|---|
| Diluted weighted-avg shares outstanding | | | | |
| Basic weighted-avg shares outstanding | | | | |

**Read:**
- **Down YoY** = buybacks more than offset SBC and any other dilution → real per-share return to shareholders.
- **Flat YoY** = buybacks roughly offsetting dilution → "treadmill"; capital is being recycled to employees rather than returned to shareholders.
- **Up YoY** = net dilution; either no buyback program, or SBC plus any secondary / convert / acquisition-related issuance is overwhelming repurchases.

Cross-check against the buyback dollar spend above: if buyback $ is meaningful but share count is still flat or up, the dilution rate from SBC and other issuance is exceeding the repurchase yield — flag the gap explicitly.

##### Forward share-count guide (if disclosed)

Some companies telegraph an end-of-FY (or end-of-period) diluted share count target — either directly, or implied via EPS and net-income guidance. Capture this as a forward dilution guide; it's the cleanest signal of what management expects net buyback / SBC dynamics to look like through year-end.

| Item | Current | FY-End Guide | Implied Δ from Current | Implied Δ% | Prior Quarter's Guide for Same FY End |
|---|---|---|---|---|---|
| Diluted weighted-avg shares (FY end) | | | | | |
| Implied net dilution / (anti-dilution) rate (annualized) | — | | — | | — |

**Read:**
- **FY-end guide implies further share-count reduction** = buyback pace expected to outpace SBC through year-end; thesis-positive for per-share metrics.
- **FY-end guide implies share count roughly flat** = dilution treadmill expected to continue.
- **FY-end guide implies share count growth** = net dilution baked into the plan; check whether driven by continued SBC, a planned acquisition (stock consideration), a convertible bond dilution event, or a known secondary / ATM.

**Track changes vs. prior guide:** If the FY-end target was raised vs. last quarter's guide, dilution is running hotter than expected or buyback pace has slowed — flag. If lowered, repurchase pace is ahead of plan. Either direction is a meaningful signal even when the absolute number is small.

**If share count is not explicitly guided** but EPS and net income (or operating income with a tax-rate guide) are, back into an implied diluted share count: `implied shares ≈ guided net income / guided EPS`. Mark this as a derived figure rather than a direct disclosure, and note the assumption used.

In 1–2 sentences, characterize the period's capital allocation posture (returning cash to shareholders / reinvesting / deleveraging / refinancing / accumulating cash) — and whether the trailing YoY share count change AND the forward FY-end share-count guide are consistent with that posture.

#### 3h. Management Commentary & Tone
- Key themes from CEO/CFO prepared remarks
- Any notable language shifts vs. prior quarters (more cautious? more bullish?)
- Analyst Q&A highlights: what questions dominated? What did management avoid?
- Watch for: hedging language, macro commentary, competitive remarks, product roadmap hints

#### 3i. Stock Reaction Context
- Day-of stock move (if known or provided)
- Was the move consistent with the fundamental result, or a setup/expectation issue?
- Brief note on what drove market reaction (e.g., guidance cut despite beat, or margin upside)

---

### Step 4 — Bottom Line

End with a 3–5 sentence synthesis:
- Was this a good quarter overall?
- What's the most important takeaway for the investment thesis?
- What are 1–2 things to watch in coming quarters?

---

## Output Format

- Start with **Company Context** (2–3 sentences)
- Then the **Scorecard table**
- Then **Detailed Sections** (3a through 3i) with clear headers
- End with **Bottom Line**
- Use tables where data is comparative (segments, guidance)
- Be concise within sections — prioritize insight over exhaustive description

---

## Step 5 — Industry & Company Module

After completing the core analysis, check whether a specialized module applies.

### How to identify the industry
Use the company name, ticker, or document content to classify the industry. If ambiguous, use the largest revenue segment.

### Industry modules (read the relevant file before proceeding)

| Industry | Trigger keywords / examples | Module file |
|---|---|---|
| Telecom | wireless, postpaid, ARPU, fiber, FWA, spectrum, 5G | `modules/telecom.md` |

### Company-specific modules (read if the company matches)

| Company | Ticker | Module file |
|---|---|---|
| AT&T | T | `modules/att.md` |
| Carvana | CVNA | `modules/cvna.md` |

### Universal modules (load for every earnings analysis)

| Module | When to load | Module file |
|---|---|---|
| Valuation | Always — load for every earnings analysis | `modules/valuation.md` |

### Routing logic
1. **Always** load `modules/valuation.md` — it runs for every company.
2. Check for a **company-specific module** — if one exists, read it. It may override or extend the industry module.
3. If no company-specific module exists but an **industry module** matches, read that instead.
4. If neither applies, complete only the core 8-section analysis + valuation.

### Output order
Core sections (1–4) → Bottom Line → Industry/Company module sections → Valuation module

When a module is loaded, append its output as clearly labelled additional sections — do not replace any core sections.

---

## Notes

- If slides or transcript are not provided, note what's missing and proceed with available documents
- If a metric is not disclosed, say so rather than leaving a blank
- For non-US companies, note currency and any FX impact on growth rates
- IOMA is Yi's custom framework — always run it unless the user says to skip it
- Always check for an applicable module — industry or company-specific — before finalising output
