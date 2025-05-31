import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load Excel files
file_paths = {
    "All_Vendor_Data": "data/BC Hydro - All Vendor Data.xlsx",
    "Category_Description": "data/BC Hydro - Category Description.xlsx",
    "SC_Risk_Tolerance": "data/BC Hydro - SC risk tolerance by category.xlsx",
    "Vendor_Inventory_Data": "data/BC Hydro - Vendor and Inventory Data.xlsx"
}

# Read sheets
vendor_df = pd.read_excel(file_paths["All_Vendor_Data"])
category_df = pd.read_excel(file_paths["Category_Description"], sheet_name="Cat Subcat List - Full")
risk_df = pd.read_excel(file_paths["SC_Risk_Tolerance"], sheet_name=0)
inventory_df = pd.read_excel(file_paths["Vendor_Inventory_Data"])

# Print column names for debugging
print("Vendor DF Columns:", vendor_df.columns.tolist())
print("Category DF Columns:", category_df.columns.tolist())
print("Risk DF Columns:", risk_df.columns.tolist())
print("Inventory DF Columns:", inventory_df.columns.tolist())

# --- Standardize column names ---

# Vendor and Inventory: unify "Category Name"
vendor_df.rename(columns={"Category Name": "Category"}, inplace=True)
inventory_df.rename(columns={"Category NAME": "Category"}, inplace=True)

# Risk: unify column casing and strip whitespace
risk_df.rename(columns={
    "CATEGORY": "Category",
    "PORTFOLIO": "Portfolio",
    "Risk Tolerance of the category": "Risk tolerance of the category"
}, inplace=True)

# Category metadata: unify "Category NAME"
category_df.rename(columns={"Category NAME": "Category"}, inplace=True)

# --- Merge datasets ---

# 1. Merge vendor + inventory
merged_df = pd.merge(vendor_df, inventory_df, on="Reference #", how="left")

# 2. Merge risk info
merged_df = pd.merge(merged_df, risk_df[["Category", "Risk tolerance of the category", "Portfolio"]], on="Category", how="left")

# 3. Optionally merge category metadata
if "Sub-Category" in category_df.columns:
    merged_df = pd.merge(merged_df, category_df[["Category", "Sub-Category"]], on="Category", how="left")

# --- Output result ---

# Print a preview of the final merged data
print("\nMerged Data Columns:")
print(merged_df.columns.tolist())
print("\nMerged Data Sample:")
print(merged_df.head())
