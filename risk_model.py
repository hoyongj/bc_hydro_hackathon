# risk_model.py
"""Build composite risk scores + what-if tariff scenario."""
import numpy as np
import pandas as pd
import config
from data_prep import (
    load_vendor_inventory,
    load_all_vendors,
    load_risk_tolerance,
    load_lpi,
)

# ------------------------------------------------------------------ #
# helpers
# ------------------------------------------------------------------ #
def _scale(s: pd.Series, kind: str = "minmax") -> pd.Series:
    if kind == "zscore":
        mu, sigma = s.mean(), s.std(ddof=0)
        return (s - mu) / sigma if sigma else s * 0
    lo, hi = s.min(), s.max()
    return (s - lo) / (hi - lo) if hi > lo else s * 0


# ------------------------------------------------------------------ #
# internal metrics
# ------------------------------------------------------------------ #
def _internal_scores(inv_path, vendor_path) -> pd.DataFrame:
    inv = load_vendor_inventory(inv_path)
    v   = load_all_vendors(vendor_path)

    g_inv = inv.groupby("category_name").agg(
        avg_lead_time=("average_lead_time_(days)", "mean"),
        lead_time_sd=("standard_deviation_of_lead_time_(days)", "mean"),
        days_of_supply=("days_of_supply_(current)", "mean"),
    )

    vendor_tot = v.groupby("category_name")["vendornumber_clean"].nunique()
    vendor_us  = (
        v[v["restrictedusvendor"] == "Y"]
        .groupby("category_name")["vendornumber_clean"]
        .nunique()
    )
    g_inv["vendor_concentration"] = 1 / vendor_tot
    g_inv["us_dependency"]        = vendor_us.div(vendor_tot).fillna(0)

    g_inv["lead_time_cv"] = g_inv["lead_time_sd"].div(g_inv["avg_lead_time"].replace({0: np.nan})).fillna(0)

    # min-max all the raw columns so every sub-score is on 0-1 scale
    for col in ["avg_lead_time", "lead_time_cv", "vendor_concentration", "days_of_supply"]:
        g_inv[f"scaled_{col}"] = _scale(g_inv[col], kind=config.SCALING)

    return g_inv.reset_index()


# ------------------------------------------------------------------ #
# external metrics
# ------------------------------------------------------------------ #
def _external_scores(inv_path, lpi_path) -> pd.DataFrame:
    """Return only the logistics score; leave US-dependency to _internal_scores()."""
    inv = load_vendor_inventory(inv_path)
    lpi = load_lpi(lpi_path)[["country_name", "lpi_score"]]

    inv = inv.merge(
        lpi, left_on="country_of_origin", right_on="country_name", how="left"
    )
    # avoid chained-assignment warning
    inv["lpi_score"] = inv["lpi_score"].fillna(lpi["lpi_score"].median())

    g = (
        inv.groupby("category_name")["lpi_score"]
        .mean()
        .reset_index()
        .rename(columns={"lpi_score": "avg_lpi"})
    )

    g["scaled_logistics"] = 1 - _scale(g["avg_lpi"], kind=config.SCALING)
    return g[["category_name", "scaled_logistics"]]


# ------------------------------------------------------------------ #
# public API
# ------------------------------------------------------------------ #
def build_risk_table(inv_path, vendor_path, tol_path, lpi_path) -> pd.DataFrame:
    internal = _internal_scores(inv_path, vendor_path)
    external = _external_scores(inv_path, lpi_path)

    tol = load_risk_tolerance(tol_path)[
        ["category", "risk_tolerance_of_the_category"]
    ].rename(
        columns={
            "category": "category_name",
            "risk_tolerance_of_the_category": "risk_tolerance",
        }
    )

    df = (
        internal.merge(external, on="category_name", how="left")
        .merge(tol, on="category_name", how="left")
    )
    df["risk_tolerance"].fillna("Med", inplace=True)

    # weighted component scores
    df["internal_score"] = (
        df["scaled_avg_lead_time"] * config.INTERNAL_WEIGHTS["lead_time"]
        + df["scaled_lead_time_cv"] * config.INTERNAL_WEIGHTS["lead_time_cv"]
        + df["scaled_vendor_concentration"]
        * config.INTERNAL_WEIGHTS["vendor_concentration"]
        + df["scaled_days_of_supply"] * config.INTERNAL_WEIGHTS["days_of_supply"]
    )

    df["external_score"] = (
        df["scaled_logistics"] * config.EXTERNAL_WEIGHTS["logistics"]
        + df["us_dependency"] * config.EXTERNAL_WEIGHTS["us_dependency"]
    )

    df["base_risk_score"] = (df["internal_score"] + df["external_score"]) / 2

    df["adjusted_risk_score"] = df.apply(
        lambda r: r["base_risk_score"]
        * config.RISK_TOLERANCE_MULTIPLIER.get(r["risk_tolerance"], 0.85),
        axis=1,
    )

    return df


def apply_us_tariff_scenario(df: pd.DataFrame, add_pct: float = 25.0) -> pd.DataFrame:
    """Extra bump for categories that rely >50 % on U.S. vendors."""
    df = df.copy()
    bump_factor = 1 + add_pct / 100
    df["scenario_risk_score"] = df["adjusted_risk_score"] + (
        df["us_dependency"].where(df["us_dependency"] > 0.5, 0) * (bump_factor - 1)
    )
    return df
