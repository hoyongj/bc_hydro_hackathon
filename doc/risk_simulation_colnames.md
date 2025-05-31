## 1 · Column-by-column cheat-sheet

| column                      | meaning                                                                                     | notes on scale / direction                  |
| --------------------------- | ------------------------------------------------------------------------------------------- | ------------------------------------------- |
| **category\_name**          | BC Hydro material category.                                                                 | key for grouping.                           |
| **avg\_lead\_time**         | Mean calendar days between PO and delivery (internal data).                                 | higher → riskier.<br>raw, not scaled.       |
| **lead\_time\_sd**          | Standard deviation of lead time.                                                            | raw.                                        |
| **days\_of\_supply**        | Current stock ÷ average daily usage.                                                        | raw.                                        |
| **vendor\_concentration**   | `1 / (# unique vendors)` for the category.                                                  | 1 = single-source.                          |
| **us\_dependency**          | Share of vendors whose “restrictedUSvendor = Y”.                                            | 0–1.                                        |
| **lead\_time\_cv**          | Coefficient of variation = `lead_time_sd / avg_lead_time`.                                  | unit-free instability indicator.            |
| **scaled\_* columns*\*      | Min-max normalisations (0 = best in class, 1 = worst) so we can weight apples with oranges. | derived on the fly each run.                |
| **scaled\_logistics**       | `1 – minmax(LPI)` ⇒ poor infrastructure ↔ 1.                                                | data from World Bank 2023 LPI.              |
| **risk\_tolerance**         | Qualitative appetite set by BC Hydro SC team (High / Med / Low).                            | drives a multiplier.                        |
| **internal\_score**         | Weighted sum of the four internal scaled metrics using `config.INTERNAL_WEIGHTS`.           | range ≈ 0–1.                                |
| **external\_score**         | Weighted sum of `scaled_logistics` + `us_dependency`.                                       | range ≈ 0–1.                                |
| **base\_risk\_score**       | Simple mean of internal & external.                                                         | your “raw” risk.                            |
| **adjusted\_risk\_score**   | `base_risk_score × tolerance multiplier` (High = 1.00, Med = 0.85, Low = 0.70).             | **Primary ranking column** in the base run. |
| **scenario\_risk\_score**\* | Only appears when you run a scenario; see below.                                            |                                             |

---

## 2 · How the numbers are built

1. **Min-max scaling**
   For every numeric driver we find the global min & max across all categories, then map

   $$
     \text{scaled} = \frac{x - x_{min}}{x_{max} - x_{min}}
   $$

   so everyone sits on a comparable 0-1 axis.

2. **Internal composite**

   $$
     S_{\text{internal}} =
       0.40\;(\text{lead-time}) +
       0.20\;(\text{lead-time CV}) +
       0.20\;(\text{vendor conc.}) +
       0.20\;(\text{days-of-supply})
   $$

3. **External composite**

   $$
     S_{\text{external}} =
       0.50\;(\text{logistics}) +
       0.30\;(\text{U.S. dependency})
   $$

4. **Raw risk**

   $$
     S_{\text{base}} = \tfrac12\bigl(S_{\text{internal}} + S_{\text{external}}\bigr)
   $$

5. **Risk-tolerance overlay**
   *High* tolerance leaves the score untouched; *Med* shaves 15 %; *Low* shaves 30 %.
   This yields **`adjusted_risk_score`**, the one you usually sort by.

---

## 3 · Simulation logic (“25 % U.S. tariff”)

When you call

```bash
python main.py --scenario us_tariff_25pct
```

`risk_model.apply_us_tariff_scenario()` does three things:

1. **Identify affected categories** – those where **`us_dependency > 0.5`** (i.e. more than half the vendor count is U.S.-based).

2. **Compute a bump factor** –

$$
\text{bump} =  \frac{25}{100} = 0.25
$$

3. **Add the incremental risk** –

$$
S_{\text{scenario}} = S_{\text{adjusted}} + \bigl(\text{US-Dependency} \times 0.25\bigr)
$$

   so a category that is 80 % reliant on U.S. vendors picks up an extra
   $0.8 × 0.25 = 0.20$ absolute-risk points.

The result lands in **`scenario_risk_score`**; categories under the 50 % threshold stay unchanged, letting you zero-in on the most tariff-sensitive portfolios.

*(If you like a gentler shock, just add `--scenario us_tariff_10pct` after wiring that variant into `config.SCENARIOS`.)*

---

## 4 · Reading the output file

1. **Open** the CSV (first 15 rows shown above).
2. **Sort descending on `adjusted_risk_score`** (or `scenario_risk_score` if you ran the tariff case).
3. **Interpret tiers** (example thresholds – tweak to taste):

| score       | tier               | action                                                                  |
| ----------- | ------------------ | ----------------------------------------------------------------------- |
| ≥ 0.60      | **Red / high**     | Immediate mitigation project (dual source, inventory uplift, redesign). |
| 0.40 – 0.59 | **Amber / medium** | Monitor KPIs, prep contingent levers.                                   |
| < 0.40      | **Green / low**    | BAU; revisit quarterly.                                                 |

Because every component is 0-1, the composites land roughly 0-1 too; under tariff shocks they can exceed 1 for the most exposed categories.

---

## 5 · Customising / extending

* **Add HS-code tariff data** – merge your category→HS lookup, scale the tariff column, and plug it into `EXTERNAL_WEIGHTS`.
* **Swap scaling method** – flip `SCALING = "zscore"` in `config.py` for standard-score scaling.
* **Play with weights** – all dials live in `config.py`; rerun for instant what-ifs.
* **Visualise** – read the CSV into Power BI / Tableau or attach a simple Streamlit dashboard.

That’s all you need to interpret the output and understand the simulation engine. Fire away if you want deeper dives or new scenarios!
