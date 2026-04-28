# Peer Comparison Module

Use this module when 2+ providers are in scope. Goal is a **side-by-side scorecard** that surfaces relative performance and competitive dynamics across providers, not a re-derivation of individual provider data.

This module consumes per-provider data already extracted (via the sibling `telecom-provider-analysis` skill — its Snapshot Card and Detail sections supply the source figures). If snapshots are not yet built, run that skill against each provider first, then load this module.

---

## Comparison Output Structure

### Section 1 — Provider Snapshot References (compact)

For each in-scope provider, surface a tight reference card — either by reproducing the Snapshot Card from the corresponding `telecom-provider-analysis` output or building a compact equivalent. Display in this order:

1. AT&T (if present)
2. Verizon (if present)
3. T-Mobile (if present)
4. Comcast (if present)
5. Charter (if present)

Keep each card scannable — this is for orientation, not the main artifact.

### Section 2 — Side-by-Side Scorecard

The core comparison artifact. Use this table structure (drop columns for providers not in scope):

#### 2a. Wireless / Mobile

| Metric | AT&T | Verizon | T-Mobile | Comcast | Charter |
|---|---|---|---|---|---|
| Postpaid phone net adds | | | | n/a* | n/a* |
| Mobile line net adds (MVNO) | n/a | n/a | n/a | | |
| Postpaid phone churn | | | | n/a | n/a |
| Postpaid / mobile ARPU | | | | | |
| Wireless service revenue growth | | | | n/a | n/a |
| EBITDA service margin | | | | n/a | n/a |

*For Comcast/Charter, mobile is reported as lines, not postpaid phone — populate the line below.

#### 2b. Broadband / Fixed

| Metric | AT&T | Verizon | T-Mobile | Comcast | Charter |
|---|---|---|---|---|---|
| Total broadband net adds | | | | | |
| Fiber net adds | | | n/a (small via JV) | n/a | n/a |
| FWA net adds | (small) | | | n/a | n/a |
| Broadband ARPU | | | | | |
| Fiber/HFC subs total | | | | | |
| Convergence / bundle attach | | | | | |

#### 2c. Financials

| Metric | AT&T | Verizon | T-Mobile | Comcast | Charter |
|---|---|---|---|---|---|
| Revenue (period) | | | | | |
| Revenue YoY growth | | | | | |
| EBITDA margin | | | | | |
| Capex intensity | | | | | |
| FCF | | | | | |
| FCF margin | | | | | |
| Net debt / EBITDA | | | | | |
| Capital return (div + bb) | | | | | |

### Section 3 — Winners & Losers Commentary

For each major dimension, identify the relative winner and laggard with a one-sentence "why":

- **Postpaid phone share**: who took the most net adds? (Big 3 only, but flag if cable mobile is bleeding the Big 3)
- **Broadband share**: who's gaining and at whose expense? Map cable losses to fiber/FWA gains where possible
- **ARPU power**: who's pushing pricing through, who's holding flat, who's giving back via promos
- **Margin profile**: who's expanding, who's compressing, why
- **Capital intensity**: who's in invest mode, who's in harvest mode
- **Balance sheet**: who's deleveraging, who's leveraging, who's most exposed to rates

### Section 4 — Cross-Cutting Dynamics

Identify 2–4 dynamics that show up across providers — these are the comparison's analytical payoff:

- **Wireless → broadband substitution**: how much of cable's broadband loss is going to FWA? Tie cable broadband net adds to Verizon + T-Mobile FWA net adds quantitatively if data allows.
- **Cable mobile → Big 3 pressure**: are Comcast/Charter mobile net adds explaining any Big 3 postpaid weakness?
- **Fiber overbuild**: are AT&T fiber adds in markets where Comcast/Charter operate? Geographic overlap commentary if disclosed.
- **Convergence race**: who's winning bundled customers? Is the convergence trade lifting any provider's churn meaningfully?
- **Promotional intensity**: directional read across providers — are promos escalating or rationalizing?
- **Capex cycle position**: are providers converging on a post-buildout / harvest-mode FCF inflection?

### Section 5 — Bottom Line

3–5 sentences synthesizing the comparative picture:
- Who had the strongest quarter and why
- Who's facing the most pressure and from whom
- The single most important share or pricing dynamic to watch next quarter

---

## Comparison Notes

- **Period alignment**: providers may report on different cadences or fiscal calendars. Always state each provider's period at the top of the comparison and note any apples-to-oranges comparisons.
- **Reporting differences**: Big 3 break out wireless/wireline in segments; cable breaks out connectivity/business/(content); be precise about which figure is being compared. Don't compare AT&T total revenue to Comcast total revenue without flagging the NBCU + parks distortion in Comcast's number — use Comcast Connectivity & Platforms revenue for cleaner comparison.
- **ARPU comparability**: postpaid phone ARPU (Big 3) is conceptually different from cable mobile ARPU — note this when comparing.
- **Be quantitative where possible**, qualitative where data is missing. Don't manufacture precision.
- **Don't grade every metric.** Pick the 3–5 most consequential dimensions for the period and concentrate the analysis there.
