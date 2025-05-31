import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.colors as mcolors

MODE_NAME = "base"
df = pd.read_csv(f"risk_scores_{MODE_NAME}.csv")

# Mapping dictionary (already provided by you)
category_to_portfolio = {
    "Major Gen Powerhouse": "Major Equipment & Construction (Peter Kobzar)",
    "Meters": "Material & Logistics (Mark Robinson)",
    "Switchgear": "Major Equipment & Construction (Peter Kobzar)",
    "Protect/ControlEquip": "Major Equipment & Construction (Peter Kobzar)",
    "Battery Energy Strge": "Major Equipment & Construction (Peter Kobzar)",
    "Distribution Transf": "Material & Logistics (Mark Robinson)",
    "Wire And Cable": "Material & Logistics (Mark Robinson)",
    "Oth Gen Stn Equip": "Major Equipment & Construction (Peter Kobzar)",
    "Telecom": "Engineering & Technical Services (Gareth Clarke)",
    "Telecom Equip": "Engineering & Technical Services (Gareth Clarke)",
    "EV Equip & Services": "Engineering & Technical Services (Gareth Clarke)",
    "Electrical Component": "Material & Logistics (Mark Robinson)",
    "Power Transformer": "Major Equipment & Construction (Peter Kobzar)",
    "Fleet": "Material & Logistics (Mark Robinson)",
    "IT": "Enterprise (Jennifer Sonnenberg)",
    "Aux Elec Equip": "Major Equipment & Construction (Peter Kobzar)",
    "MRO-Gen Indus/Safety": "Material & Logistics (Mark Robinson)",
    "Metering & Network": "Material & Logistics (Mark Robinson)",
    "Fuel, Oil, Lubricant": "Material & Logistics (Mark Robinson)",
    "Pre-Cast Concrete": "Material & Logistics (Mark Robinson)",
    "Construct Material": "Material & Logistics (Mark Robinson)",
    "Utility Tools/Equip": "Material & Logistics (Mark Robinson)",
    "Construction Equip": "Field Support Services (Adele Neuman)",
    "Chemicals and Gases": "Material & Logistics (Mark Robinson)",
    "Conductor Supp Struc": "Material & Logistics (Mark Robinson)",
}

# Apply portfolio mapping
df['portfolio'] = df['category_name'].map(category_to_portfolio)

# Sort by risk score
df_sorted = df.sort_values("scenario_risk_score", ascending=True)

# Generate pastel colors
base_colors = cm.get_cmap('tab10').colors
pastel_colors = [[(r + 1) / 2, (g + 1) / 2, (b + 1) / 2] for (r, g, b) in base_colors]

# Assign pastel colors to portfolios
portfolios = df_sorted['portfolio'].unique()
portfolio_colors = dict(zip(portfolios, pastel_colors[:len(portfolios)]))
bar_colors = df_sorted['portfolio'].map(portfolio_colors)

# Plot
plt.figure(figsize=(10, 8))
bars = plt.barh(df_sorted["category_name"], df_sorted["scenario_risk_score"], color=bar_colors)
plt.xlabel("scenario_risk_score")
plt.ylabel("Category")
plt.title(f"BC Hydro – Supply-Chain Risk by Category ({MODE_NAME} Scenario)")

# Add legend
legend_handles = [plt.Line2D([0], [0], color=color, lw=6, label=portfolio)
                  for portfolio, color in portfolio_colors.items()]
plt.legend(handles=legend_handles, title="Portfolio", loc='lower right')

plt.tight_layout()
plt.show()
