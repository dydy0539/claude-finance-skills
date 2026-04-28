---
name: industry-competitive-positions
description: >
  Use this skill whenever the user wants to assess US telecom industry competitive dynamics, market
  positioning, or peer comparisons across multiple providers in the same reporting period. Sibling
  skill to `telecom-provider-analysis` — that skill produces single-company snapshots; THIS skill
  takes 2+ snapshots (or raw earnings docs from 2+ providers) and synthesizes a cross-provider
  competitive view. Covers AT&T, Verizon, T-Mobile, Comcast, Charter. Triggers: uploading earnings
  from 2+ of these providers; phrases like "compare [A] vs [B]", "Big 3 wireless dynamics", "cable
  vs telco share", "which carrier won the quarter", "industry view", "competitive landscape",
  "who's gaining share", "FWA vs fiber vs cable migration". ALSO trigger when single-provider
  snapshots already exist in the conversation and the user asks any comparative or industry-level
  question. Output is a side-by-side comparison and/or industry-wide synthesis based on framing.
---

# Industry Competitive Positions Skill

A workflow for synthesizing US telecom industry competitive dynamics from multiple providers' results in the same reporting period. The unit of analysis is **the industry**, not the individual company — assumes single-company stats have already been (or are simultaneously being) extracted via `telecom-provider-analysis`.

## Scope

This skill operates over the same five providers as `telecom-provider-analysis`:

- AT&T (T)
- Verizon (VZ)
- T-Mobile (TMUS)
- Comcast (CMCSA)
- Charter (CHTR)

Two or more providers must be present (as snapshots, earnings docs, or established context in the conversation) for this skill to do its job. With only one provider, redirect to `telecom-provider-analysis`.

---

## Inputs

This skill accepts two input types:

1. **Provider snapshots** — outputs from `telecom-provider-analysis` already produced earlier in the conversation. Most efficient — universal KPIs and idiosyncratic context are already extracted in standardized form.
2. **Raw earnings documents from 2+ providers** — if snapshots haven't been built yet. In this case, run `telecom-provider-analysis` against each provider first to produce the snapshots, then synthesize.

Always **align periods** before synthesizing — providers may report different fiscal calendars; explicitly state each provider's period and flag any apples-to-oranges comparisons.

---

## Modes

This skill has two modes that can run separately or together depending on the user's framing:

| Mode | Trigger | Output | Module |
|---|---|---|---|
| **Peer Comparison** | "compare X vs Y", 2–3 providers in scope, comparison framing | Side-by-side scorecard + winners/losers commentary | `modules/comparison.md` |
| **Industry View** | "industry dynamics", "Big 3 vs cable", 4+ providers, market-level framing | Industry structure + cross-cutting themes synthesis | `modules/industry-view.md` |

Default rules:
- 2 providers → Peer Comparison only
- 3 providers → Peer Comparison; offer Industry View as add-on
- 4+ providers → both modes (Comparison first, then Industry View)
- User explicitly asks for industry view → Industry View, regardless of provider count

---

## Workflow

### Step 1 — Inventory the Inputs

Confirm which providers' data is available and whether the inputs are snapshots (from `telecom-provider-analysis`) or raw earnings docs.

If raw earnings docs: invoke `telecom-provider-analysis` against each provider first. The snapshots become the inputs to Steps 2 and 3.

### Step 2 — Period Alignment Check

State explicitly the period each provider's data covers. If periods differ:
- Flag the misalignment to the user
- Proceed if differences are minor (e.g., all Q3 calendar quarter)
- Pause for clarification if differences are material (e.g., comparing AT&T Q3 to Verizon Q1)

### Step 3 — Run Selected Mode(s)

Load the applicable module(s):
- `modules/comparison.md` for Peer Comparison
- `modules/industry-view.md` for Industry View

Each module specifies its output structure. Don't deviate.

### Step 4 — Synthesize

Produce the output per the loaded module(s). The output should:
- Lead with the structured comparison or industry view (tables, then commentary)
- End with a short Bottom Line (3–5 sentences) that nails the most important shift in the period

### Step 5 — Save the Synthesis as a PDF

After producing the chat output, save a PDF copy via the **`analysis-snapshot-pdf`** skill so the comparison/industry view is durable across sessions. **Mandatory by default** — only skip if the user explicitly says "chat only" or "don't save."

`analysis-snapshot-pdf` owns all formatting concerns (typography, layout, fonts, page setup). This step only specifies the industry-specific bits: where the file goes, what it's named, and how to map the synthesis into that skill's block schema.

**File location:**
- Save to the workspace root (no single company folder owns an industry view), or into a dedicated `_industry/` subfolder if one already exists in the workspace.
- Do not silently overwrite an existing file for the same period — append a version suffix (e.g., `… v2.pdf`) or ask.

**Filename convention:**
- Peer Comparison: `<Tickers> Peer Comparison Q<X> <YYYY>.pdf` — e.g., `VZ vs CHTR Peer Comparison Q1 2026.pdf`. For 3+ providers, list them alphabetically separated by " vs ", or use `<N>-Way Peer Comparison Q<X> <YYYY>.pdf`.
- Industry View: `Industry Snapshot Q<X> <YYYY>.pdf` — e.g., `Industry Snapshot Q1 2026.pdf`.
- Both modes in one run: `Industry & Peer Snapshot Q<X> <YYYY>.pdf`.

**Content payload (mapping to the `analysis-snapshot-pdf` schema):**

- `title`: framed for scope — e.g., `US Telecom Q1 2026 Peer Comparison: VZ vs CHTR`, or `US Telecom Industry Snapshot — Q1 2026`
- `subtitle`: providers covered · period covered — e.g., `VZ · CHTR · Q1 2026`
- `metadata`: Period covered / Providers included / Mode(s) run / Period alignment notes (if any non-trivial misalignment was flagged in Step 2)
- `blocks`:
    1. One or more **`table`** blocks — the comparative scorecards. First column is the dimension/metric, subsequent columns are the providers. Set `highlight_first_column: true` so metric labels stand out. Lead with the most consequential dimensions for the period (typically a wireless table, a broadband table, and a financial-efficiency table — but always tailored to what's most consequential, not boilerplate).
    2. A **`sections`** block titled "Commentary" (`label_style: heading`) — analytical reads on each scorecard, with substitution math made explicit where it applies (e.g., cable broadband loss ↔ FWA + fiber gain in overlapping markets).
    3. (Industry View only) A **`sections`** block titled "Industry-wide themes" with the cross-cutting threads from `modules/industry-view.md`.
    4. A **`numbered`** block titled "Bottom Line" with the 3–5 sentences from Step 4 — bold prefix is the headline takeaway, body is the supporting one-liner.
- `footer_id`: e.g., `Peer Comparison Q1 2026 · VZ vs CHTR`, or `Industry Snapshot Q1 2026`
- `sources`: list of provider snapshots / earnings documents actually used, by ticker (e.g., `["VZ Q1 2026 Snapshot", "CHTR Q1 2026 Snapshot"]`)

Construct the dict, write to a temp JSON file, and run `analysis-snapshot-pdf`'s renderer against it (or import the renderer directly). Then surface a `computer://` link to the saved PDF in the reply.

Remember: in any string body, escape literal `&` `<` `>` as `&amp;` `&lt;` `&gt;`, but keep `<b>` / `<i>` / `<sub>` / `<super>` tags as XHTML for inline emphasis.

---

## Output Format Rules

- **Tables are central** — comparative data without tables defeats the purpose. Use them generously.
- **Be quantitative where possible, qualitative where data is missing.** Don't manufacture precision.
- **State the period** at the top of every table; flag any misaligned periods.
- **Don't grade every metric.** Pick the 3–5 most consequential dimensions for the period and concentrate analytical energy there.
- **Pull from snapshot Part D (idiosyncratic) sparingly** — comparison and industry view should focus on universal KPIs that are actually comparable across providers. Idiosyncratic items get mentioned only when they materially affect a comparison (e.g., FirstNet contribution to AT&T's wireless growth, Frontier deal pro forma for Verizon, Charter rural passings adding to footprint growth).
- **Always finish by saving the synthesis as a PDF per Step 5** (unless the user opts out) and surface the file link.

---

## Substitution & Comparability Notes

Several structural quirks affect cross-provider comparison — these are surfaced in the modules but worth keeping front of mind:

- **Cable mobile (Comcast Xfinity, Charter Spectrum) reports "lines"** while Big 3 reports "postpaid phone net adds". Both go in the same "wireless adds" comparison row but the conceptual unit differs slightly. Sum cable lines + Big 3 postpaid for total industry wireless growth.
- **Cable mobile MVNO traffic flows through Verizon's network** — wholesale revenue from this is in Verizon's results. So cable mobile growth is partly **Verizon revenue** and partly **Big 3 retail competition**. Don't double-count.
- **Comcast consolidated revenue is distorted by NBCU + parks** — when comparing revenue / EBITDA / margins, use **Comcast Connectivity & Platforms** specifically, not consolidated.
- **T-Mobile fiber is small** — don't put weight on T-Mobile fiber when comparing fiber positions.
- **AT&T Mexico is FX-distorted** — segment growth needs constant-currency framing for fair comparison to US-only peers.
- **Period-end vs. average** — some KPIs are period-end (subs); others are flow (net adds, revenue). Don't mix.

---

## Sibling Skill Coordination

This skill works downstream of `telecom-provider-analysis`. The intended flow is:

1. As each provider reports, run `telecom-provider-analysis` to produce a single-company snapshot
2. Once 2+ snapshots in the same period exist, run **this skill** to synthesize the competitive view
3. As more providers report in the same period, re-run this skill on the larger set

If a user uploads multiple providers' docs in a single turn, it's appropriate to run `telecom-provider-analysis` on each (producing compact snapshots) and then run this skill — but flag this as a multi-step output and keep individual snapshots compact when comparison is the user's main goal.

---

## Notes & Discipline

- **Don't pad with general industry commentary** — every claim should tie back to the data in front of you. If the documents don't support a claim, don't make it.
- **Surface dynamics, not just numbers** — "Verizon postpaid net adds: +X. T-Mobile postpaid net adds: +Y" is data; "T-Mobile's lead over Verizon compressed for the third straight quarter" is the dynamic.
- **Flag your knowledge gaps** — if a metric is not disclosed by a provider but is by others, say so explicitly. Don't fabricate to fill the table.
- **The substitution math is the analytical payoff** — wherever broadband or wireless customers are migrating between providers, try to make the math explicit (cable broadband loss ≈ FWA + fiber gain in overlapping markets, etc.). Even directional / qualitative substitution analysis is high-value.
