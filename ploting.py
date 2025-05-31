import pandas as pd
import matplotlib.pyplot as plt

# df = pd.read_csv("risk_scores_base.csv")
df = pd.read_csv("output.csv")

# Sort so the highest-risk items land at the top of the chart
df_sorted = df.sort_values("scenario_risk_score", ascending=True)

plt.figure(figsize=(10, 8))
plt.barh(df_sorted["category_name"], df_sorted["scenario_risk_score"])
plt.xlabel("scenario_risk_score")
plt.ylabel("Category")
plt.title("BC Hydro – Supply-Chain Risk by Category (Base Scenario)")
plt.tight_layout()
plt.show()
