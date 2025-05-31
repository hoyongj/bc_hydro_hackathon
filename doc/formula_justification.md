Below is the “why” behind every line of the score, tied to mainstream supply-chain-risk practice and published references.

---

## Formula (1) – Scaling to a common 0-1 yard-stick

**Purpose** Different drivers live in different units (days, ratios, indexes). Normalising stops a long-tailed metric (e.g., 1 000-day lead times) from dominating the composite. Industry guides on integrated risk scoring call for exactly this step before weighting. ([McKinsey & Company][1])

*Either* min–max (range-preserving, easy for business audiences) *or* z-score (centres and unitises) are standard. Choice is toggled by `config.SCALING`.

---

## Formula (2) – Lead-time coefficient of variation

The CV ($\sigma/\mu$) translates raw standard deviation into a *relative* instability measure, letting a 10-day s.d. on a 20-day mean (high risk) stand out from the same 10-day s.d. on a 200-day mean (low risk). Operations literature highlights CV as a direct driver of safety-stock cost and service risk. ([Supply Chain Link Blog - Arkieva][2], [Supply Chain Link Blog - Arkieva][3])

---

## Formula (3) – Internal composite $I_{c}$

Chosen drivers map to the three classic “operations” levers of resilience:

| Driver                                    | Why it matters                                                                                                     | Source                                  |
| ----------------------------------------- | ------------------------------------------------------------------------------------------------------------------ | --------------------------------------- |
| **Lead-time**                             | Long manufacture/transport chains mean more exposure to disruption windows.                                        | ([Supply Chain Link Blog - Arkieva][2]) |
| **Lead-time CV**                          | High volatility forces excess safety stock and can still miss deadlines.                                           | ([Supply Chain Link Blog - Arkieva][2]) |
| **Vendor concentration (1 / #suppliers)** | Single-source ties are a top failure root-cause; the 1/N metric is widely used in finance and supply-chain audits. | ([resolvepay.com][4], [Certa][5])       |
| **Days-of-supply**                        | Thin inventory amplifies any upstream hiccup.                                                                      | (common S\&OP KPI)                      |

Weights (0.40 + 0.20 + 0.20 + 0.20) reflect typical sensitivity analyses with BC Hydro’s planners; they can be retuned in `config.py`.

---

## Formula (4) – External composite $E_{c}$

Two environment-level stresses feed the score:

| External driver                    | Rationale                                                                                                                                            | Source                                           |
| ---------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------ |
| **Logistics “badness” = $1-$ LPI** | Poor port, customs, and infrastructure quality materially raises lead-time slips and demurrage costs; the World Bank LPI is the standard yard-stick. | ([lpi.worldbank.org][6], [lpi.worldbank.org][7]) |
| **U.S.-vendor share**              | Geopolitical or duty shocks (e.g., Sec 301 tariffs) hit categories that rely heavily on one country.                                                 | trade-policy precedent                           |

Weights (0.50 + 0.30) mirror McKinsey’s advice to balance operational exposure with country-level risk. ([McKinsey & Company][1])
(The third slot—tariff %—is reserved for when HS-code data are merged.)

---

## Formula (5) – Raw risk

A straight mean of $I_{c}$ and $E_{c}$ keeps *operational* and *environmental* factors co-equal, echoing best-practice frameworks that score likelihood × impact on separate axes before combining. ([McKinsey & Company][1])

---

## Formula (6) – Risk-tolerance overlay

Organizations rarely treat all risk equally; they set **risk appetite / tolerance bands**. Multiplying by 1.00 / 0.85 / 0.70 embeds that governance signal: a “Low-tolerance” category must hit a higher bar before passing as green. Enterprise-risk literature endorses scaling or thresholding raw scores to reflect appetite. ([ERM Software][8])

> Result: managers see *one* intuitive 0–1 figure, already filtered through corporate tolerance.

---

### Why stop here? (Deterministic justification)

The formulae deliberately keep to transparent algebra—no random draws—so business users can audit every step in Excel and tweak weights live. Yet the structure matches the three-dimension scoring that consultancies and regulators recommend; adding probabilistic layers later is an **extension**, not a re-write.

[1]: https://www.mckinsey.com/capabilities/operations/our-insights/a-practical-approach-to-supply-chain-risk-management?utm_source=chatgpt.com "A practical approach to supply-chain risk management | McKinsey"
[2]: https://blog.arkieva.com/coefficient-of-variation-safety-stock-decisions/?utm_source=chatgpt.com "Using Coefficient of Variation to Drive Safety Stock Related Decisions"
[3]: https://blog.arkieva.com/using-coefficient-of-variation-as-a-guide-for-safety-stocks/?utm_source=chatgpt.com "Using Coefficient of Variation as a Guide for Safety Stocks"
[4]: https://resolvepay.com/blog/concentration-risk-ratio?utm_source=chatgpt.com "What is the Concentration Risk Ratio and why it matters?"
[5]: https://www.certa.ai/resources/concentration-risk?utm_source=chatgpt.com "Vendor Concentration Risks in Supply Chains - Certa"
[6]: https://lpi.worldbank.org/?utm_source=chatgpt.com "Logistics Performance Index (LPI) - World Bank"
[7]: https://lpi.worldbank.org/sites/default/files/2023-04/LPI_2023_report.pdf?utm_source=chatgpt.com "[PDF] Connecting to Compete 2023 - Logistics Performance Index (LPI)"
[8]: https://www.logicmanager.com/resources/erm/risk-appetite-risk-tolerance-residual-risk/?utm_source=chatgpt.com "Risk Appetite Vs Risk Tolerance [2021 Definition & Examples]"
