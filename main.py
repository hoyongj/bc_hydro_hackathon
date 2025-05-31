# main.py
"""CLI entry-point."""
import argparse
from pathlib import Path
from risk_model import build_risk_table, apply_us_tariff_scenario

DEFAULT_VENDOR_INV = "BC Hydro - Vendor and Inventory Data.xlsx"
DEFAULT_ALL_VENDOR = "BC Hydro - All Vendor Data.xlsx"
DEFAULT_TOLERANCE  = "BC Hydro - SC risk tolerance by category.xlsx"
DEFAULT_LPI        = "Logistics Performance Index (LPI) - 2023.xlsx"

def _args():
    p = argparse.ArgumentParser("BC Hydro risk scorer")
    p.add_argument("--data-dir", default="./data", help="folder that holds the Excel files")
    p.add_argument("--scenario", choices=["base", "us_tariff_25pct", "us_tariff_50pct"], default="base")
    p.add_argument("--out", default="risk_scores.csv")
    return p.parse_args()

def main():
    a   = _args()
    d   = Path(a.data_dir)

    df  = build_risk_table(
        d / DEFAULT_VENDOR_INV,
        d / DEFAULT_ALL_VENDOR,
        d / DEFAULT_TOLERANCE,
        d / DEFAULT_LPI,
    )

    if a.scenario == "base":
        df = apply_us_tariff_scenario(df, add_pct=0.0)

    if a.scenario == "us_tariff_25pct":
        df = apply_us_tariff_scenario(df, add_pct=25.0)

    if a.scenario == "us_tariff_50pct":
        df = apply_us_tariff_scenario(df, add_pct=50.0)

    df.sort_values("adjusted_risk_score", ascending=False).to_csv(a.out, index=False)
    print(f"✓ Results written to {a.out}")

if __name__ == "__main__":
    main()
