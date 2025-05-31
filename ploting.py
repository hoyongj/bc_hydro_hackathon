import pandas as pd
import matplotlib.pyplot as plt

MODE_NAME = "base"
# MODE_NAME = "tariff25"

df = pd.read_csv(f"risk_scores_{MODE_NAME}.csv")
df2 = pd.read_excel("data/BC Hydro - Category Description.xlsx")

# Sort so the highest-risk items land at the top of the chart
df_sorted = df.sort_values("scenario_risk_score", ascending=True)

plt.figure(figsize=(10, 8))
plt.barh(df_sorted["category_name"], df_sorted["scenario_risk_score"])
plt.xlabel("scenario_risk_score")
plt.ylabel("Category")
plt.title(f"BC Hydro – Supply-Chain Risk by Category ({MODE_NAME} Scenario)")
plt.tight_layout()
plt.show()
