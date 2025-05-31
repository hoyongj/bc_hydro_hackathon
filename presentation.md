## 1 | Why we’re here

* BC Hydro sources **critical equipment** from dozens of countries and vendors.
* Recent shocks (COVID, geopolitics, tariffs) proved that *price* alone isn’t enough—**resilience** now matters.
* Our goal: **quantify hidden supply-chain risk** and show leaders *where* to act *first*.

---

## 2 | The core challenge — risk is multi-dimensional

| Operational                                                                            | External                        | Strategic                                  |
| -------------------------------------------------------------------------------------- | ------------------------------- | ------------------------------------------ |
| Long/unstable lead times                                                               | Port congestion, poor logistics | Over-dependence on one nation (e.g., U.S.) |
| Single-source vendors                                                                  | Sudden tariffs & trade rules    | Low corporate risk tolerance               |
| Traditionally these stay in separate spreadsheets, so no one sees the *total* picture. |                                 |                                            |

---

## 3 | Why we built a **simulation** instead of another static report

1. **Future-proofing** – lets us ask “What if a 25 % tariff hits tomorrow?” before it actually does.
2. **Objectivity** – moves debate from *opinions* to **scored evidence**.
3. **Speed** – new scenarios run in seconds; leaders can test answers live.

> Think of it as a *flight simulator* for supply-chain decisions.

---

## 4 | What we feed the model (no PhD required)

**Internal facts**

* Lead-time history
* Days of supply on hand
* Number of qualified vendors

**External signals**

* World-Bank Logistics Performance Index
* Import concentration by country
* WTO tariff database

> They’re all everyday Excel sheets—our code just stitches them together.

---

## 5 | How the score is built (plain-English view)

1. **Normalize** each metric to a simple 0–1 “badness” scale.
2. **Blend** internal health (50 %) with external exposure (50 %).
3. **Adjust** for BC Hydro’s *risk appetite* (Low → stricter, High → looser).

Result → **one composite number per category**.

* 0.0 = strong, 1.0 = fragile

---

## 6 | Base-case snapshot (today’s risk landscape)

* Top 3 red zones: *Major Gen Powerhouse, Switchgear, Battery Storage*.
* Common culprit: **year-plus lead times** + **few qualified vendors**.
* Green zones: categories with plenty of suppliers and solid logistics.

*(Detailed table is in the appendix CSV for reference.)*

---

## 7 | Scenario: “25 % U.S. tariff shock”

**What we do**

* Identify categories with > 50 % U.S. vendor reliance.
* Add a 25 % risk bump proportional to that reliance.

**Why it matters**

* Shows hidden exposure even when inventory looks healthy.
* Sparks conversation: *“Do we dual-source from Canada or Asia instead?”*

---

## 8 | Key insights leaders can act on

🔴 **Major Gen Powerhouse** – single-source + long manufacturing cycle → fast-track dual sourcing.
🟠 **Meters** – healthy today, but tariff shock pushes it into amber → renegotiate contracts early.
🟢 **Auxiliary Hardware** – stays green in every scenario → candidate for **inventory reduction**, freeing cash.

---

## 9 | Business value in dollars and sense

| Benefit                                    | Approx. impact                 |
| ------------------------------------------ | ------------------------------ |
| Prevented downtime (1 avoided outage)      | \$2–5 M / event                |
| Smarter inventory (5 % cut in green tiers) | \$3 M working-capital release  |
| Tariff-avoidance actions                   | \$1 M saved per 10 % duty hike |

Plus softer wins: regulatory confidence, ESG alignment, and calmer procurement teams.

---

## 10 | Next steps / ask

1. **Endorse** the risk score as the single language for supply-chain health.
2. **Pilot mitigations** in the three red categories this quarter.
3. **Embed** the simulator into monthly S\&OP so every new PO sees its risk early.

> Ready to fly the plane—just need your green light.
