---
name: analysis-snapshot-pdf
description: >
  Render a structured analysis snapshot (single-company, multi-company, industry view, or any
  structured research note) to a polished PDF with consistent typography. Use this whenever
  another analysis skill needs to save its output as a durable PDF artifact — e.g.,
  `telecom-provider-analysis` saving a single-company snapshot, `industry-competitive-positions`
  saving a multi-company comparison, or any future stock/sector analysis skill. Provides
  block-based rendering: header + metadata, "card" blocks (labeled groups of metric-value pairs),
  "sections" blocks (heading + body paragraphs), "numbered" blocks (numbered list with bold
  prefix), and "table" blocks (generic 2D tables for cross-entity comparisons). The caller owns
  filename and folder conventions; this skill owns formatting.
---

# Analysis Snapshot PDF Skill

A reusable formatter that takes a structured content payload and renders it to a polished PDF. Designed to be invoked by other analysis skills — separating *what to say* (caller's responsibility) from *how it's typeset* (this skill's responsibility). Adding a new sector or analysis type therefore doesn't require duplicating any formatting rules.

## When to use

Invoke this skill from another skill's "save output" step. Examples:
- `telecom-provider-analysis` → single-company operational snapshot
- `industry-competitive-positions` → multi-provider comparison
- Any future equity/sector analysis skill that wants a saved PDF artifact

Do not invoke this skill in isolation — it has no analytical content of its own. It expects a prepared content payload from the caller.

---

## Content schema

The renderer takes a JSON-serialisable dict. All string fields support a small XHTML subset for inline emphasis: `<b>…</b>`, `<i>…</i>`, `<sub>…</sub>`, `<super>…</super>`, `<br/>`. Literal `&`, `<`, `>` characters in content **must** be escaped as `&amp;`, `&lt;`, `&gt;` (this is a reportlab requirement).

```jsonc
{
  // ── Header ────────────────────────────────────────────────
  "title":    "string (required)",          // big title at top
  "subtitle": "string (optional)",          // smaller line under title (e.g. "Reported Apr 27, 2026")

  // 2-column metadata block, rendered immediately under the title
  "metadata": [
    ["label", "value"],
    ["Period reported",  "Q1 2026 (quarter ended …)"],
    ["Reporting basis",  "GAAP + non-GAAP …"],
    ["Strategic posture", "One-line framing …"]
  ],

  // ── Body — list of blocks rendered in order ──────────────
  "blocks": [
    // -- type: "card" ----------------------------------------
    // Labeled groups of metric/value pairs. Used for the "Snapshot Card".
    {
      "type": "card",
      "title": "Snapshot Card",
      "groups": [
        ["GROUP LABEL (will be uppercased)", [
          ["Metric",       "Value"],
          ["Another metric","Another value"]
        ]],
        ["NEXT GROUP", [ ["…", "…"] ]]
      ]
    },

    // -- type: "sections" ------------------------------------
    // Heading + body paragraphs. Two label styles:
    //   "heading" (default) — label rendered as a sub-heading above the body
    //   "inline"            — label rendered as bold prefix in the same paragraph as body
    // body may be a string or a list of paragraphs (strings).
    {
      "type": "sections",
      "title": "Detail",
      "label_style": "heading",
      "items": [
        ["W1. Wireless Subscribers", "Body paragraph(s) …"],
        ["W2. ARPU & Service Revenue", "Body …"]
      ]
    },
    {
      "type": "sections",
      "title": "Company-Specific Update",
      "label_style": "inline",
      "items": [
        ["Frontier integration", "Body …"],
        ["Cost transformation",  "Body …"]
      ]
    },

    // -- type: "numbered" ------------------------------------
    // Numbered list with bold prefix. Used for "Where They Stand" style sections.
    {
      "type": "numbered",
      "title": "Where They Stand",
      "items": [
        ["Bold prefix",   "Body …"],
        ["Second pillar", "Body …"]
      ]
    },

    // -- type: "table" ---------------------------------------
    // Generic 2D table. First column is highlighted by default. Used for cross-entity
    // comparisons (e.g. industry-competitive-positions).
    {
      "type": "table",
      "title": "Cross-Provider Comparison",
      "headers": ["Provider", "Postpaid net adds", "Churn", "FCF"],
      "rows": [
        ["VZ",   "+55K",  "0.97%", "$3.8B"],
        ["TMUS", "+xxxK", "x.xx%", "$x.xB"]
      ]
    }
  ],

  // ── Footer ────────────────────────────────────────────────
  "footer_id": "VZ Q1 2026 Operational Snapshot",  // shown on every page
  "sources":   ["VZ press release Q1 2026", "earnings call transcript"]  // listed in footer
}
```

---

## How to invoke

The renderer lives at `assets/render_snapshot.py` next to this file. Two ways to call it:

### CLI (preferred — language-agnostic)

```bash
# 1. Write the content payload as JSON to a temp location
cat > /tmp/snapshot_input.json <<'JSON'
{ "title": "...", "blocks": [...], "footer_id": "...", "sources": [...] }
JSON

# 2. Invoke the renderer
python3 "<this skill>/assets/render_snapshot.py" \
  --input  /tmp/snapshot_input.json \
  --output "/path/to/the/destination/Some Title.pdf"
```

### Python import (when running inside a Python script)

```python
import sys
sys.path.insert(0, "<this skill>/assets")
from render_snapshot import render

render(content_dict, "/path/to/output.pdf")
```

The renderer registers a Unicode-capable TTF (DejaVu) when available so em dashes, arrows, ≥, ≤, bullets, and curly quotes render natively. It falls back to Helvetica with reduced character coverage if no TTF font is found.

---

## Conventions the *caller* should enforce (not this skill)

This skill deliberately does NOT decide:

- **Where the PDF lives.** The caller's domain skill (e.g., `telecom-provider-analysis`) chooses the folder — typically a company-specific subfolder inside the user's workspace folder.
- **What the file is named.** The caller chooses the convention — e.g., `<TICKER> Q<X> <YYYY> Snapshot.pdf` for single-company telecom snapshots.
- **What blocks to include.** Different analyses have different shapes (single-company vs industry comparison vs research note). The caller decides which blocks to emit.

Keeping these decisions in the caller means new sectors / analysis types can adopt this renderer without modifying it.

---

## Output Format

Letter size, ~0.75" margins. Title + optional subtitle, then a metadata block, then each requested body block in order, then footer on every page (`Generated YYYY-MM-DD · <footer_id> · sources: <…>` with page number on the right).

Typography:
- Title: 15pt bold, navy
- Section heading (each block's title): 12pt bold, navy
- Sub-heading (within sections / numbered prefixes): 10.5pt bold, accent blue
- Body: 9.5pt regular, 13pt leading
- Snapshot card: 9pt with bold values; section bands rendered as navy bars

Pagination is automatic — long content flows to additional pages.

---

## Adding a new block type

To extend (e.g., add a "callout" block, a "chart" block, etc.), add a renderer branch in `assets/render_snapshot.py` keyed on `block["type"]`, and document the schema in this file.
