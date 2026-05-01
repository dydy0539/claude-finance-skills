# Valuation Module

A standalone module that can be invoked for any company. Load this module when the user asks for a valuation snapshot, "what's the stock worth", "how is it priced", or any mention of P/E, P/FCF, EV/EBITDA, dividend yield, or net cash.

This module is additive — it does not replace any core earnings sections. Append it after the core Bottom Line (and after any industry/company module).

---

## Data Sourcing

Valuation ratios require market data (price, market cap, shares outstanding) that may not be in the earnings documents. Use the following priority order:

1. **From the earnings documents** — use any per-share data, EPS, FCF per share, book value, or dividend disclosures in the press release or slides
2. **From your own knowledge** — use current price and market cap if known and recent
3. **Flag gaps** — if a ratio cannot be calculated from available data, say so explicitly rather than omitting it silently

Always state the **price and date used** for market-dependent ratios (e.g. "Based on closing price of $X on [date]").

---

## V1. Valuation Scorecard

Present as a table:

| Ratio | Value | Formula Used | Context / Interpretation |
|-------|-------|--------------|--------------------------|
| P/E (trailing) | Xx | Price ÷ TTM EPS (adj.) | |
| P/E (forward) | Xx | Price ÷ NTM EPS est. | |
| EV / EBITDA | Xx | EV ÷ TTM adj. EBITDA | |
| P / FCF | Xx | Market cap ÷ TTM FCF | |
| FCF Yield | X% | TTM FCF ÷ Market cap | Higher = more attractive |
| Price / Sales | Xx | Market cap ÷ TTM revenue | |
| Price / Book | Xx | Market cap ÷ Book value | |
| Dividend Yield | X% | Annual DPS ÷ Price | |
| Net Cash per Share | $X | (Cash − Debt) ÷ diluted shares | Negative = net debt |

For any ratio that cannot be calculated, write "n/a — [reason]" in the Value column.

---

## V2. Net Cash / Net Debt Position

- **Gross cash & equivalents** (from balance sheet)
- **Total debt** (short-term + long-term)
- **Net cash / (net debt)** = Cash − Total Debt
- **Net cash per share** = Net cash ÷ diluted shares outstanding
- Is the company's enterprise value materially different from its market cap due to net cash or net debt?
- Note: for capital-intensive or highly leveraged companies (telecom, industrials), net debt is often 2–5x EBITDA — flag if leverage looks elevated vs. sector norms

---

## V3. Earnings Power & Quality

- **TTM EPS (adjusted / non-GAAP)** vs. **GAAP EPS** — large divergence signals heavy non-cash charges or SBC
- **EPS growth rate** YoY — is the multiple justified by the growth rate? (PEG ratio = P/E ÷ EPS growth %; <1 = potentially undervalued)
- **FCF conversion** = FCF ÷ Net income; >100% = high quality earnings; <70% = investigate working capital or capex drag

---

## V4. Dividend & Capital Return (if applicable)

- **Annual dividend per share** and **dividend yield**
- **Dividend payout ratio** = DPS ÷ EPS (adj.); >75% may be unsustainable
- **FCF payout ratio** = total dividends paid ÷ FCF; the more conservative and reliable coverage test
- **Share buyback** — net shares outstanding change YoY; is the company reducing share count?
- **Total shareholder yield** = dividend yield + buyback yield

---

## V5. Valuation Context

Provide brief qualitative framing — do not just report numbers in isolation:

- Is the stock cheap or expensive vs. its own historical range? (e.g. "trades at a discount to its 5-year avg P/E of Xx")
- How does it compare to sector peers on EV/EBITDA or P/FCF? (use your knowledge; note if data is approximate)
- Does the current valuation make sense given the growth trajectory and IOMA from the core analysis?
- Any valuation catalyst or risk: upcoming index inclusion, re-rating event, leverage reduction milestone, etc.

---

## Notes

- Prefer **adjusted / non-GAAP EPS** and **adjusted EBITDA** for P/E and EV/EBITDA calculations — GAAP figures may be distorted by amortization, SBC, or one-time items
- For EV calculation: EV = Market cap + Net debt + Minority interest − Associates
- Always flag if the company has a large off-balance-sheet liability (operating leases, pension) that affects true leverage
- For companies with negative earnings, substitute EV/Revenue or EV/Gross Profit and note the substitution
