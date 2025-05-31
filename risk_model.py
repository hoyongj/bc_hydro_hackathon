# risk_model.py
"""Build composite risk scores and run what-if simulations.

Author: 2025-05-31
"""
from __future__ import annotations

from pathlib import Path
from typing import Final

import numpy as np
import pandas as pd

import config
from data_prep import (
    load_all_vendors,
    load_lpi,
    load_risk_tolerance,
    load_vendor_inventory,
)

# --------------------------------------------------------------------------- #
# Utility helpers
# --------------------------------------------------------------------------- #
def _scale(series: pd.Series, *, method: str = "minmax") -> pd.Series:
    """Return a 0-to-1 scaled version of *series*.

    Parameters
    ----------
    series : pd.Series
    method : {"minmax", "zscore"}
    """
    if method == "zscore":
        mu = series.mean()
        sigma = series.std(ddof=0)
        return (series - mu) / sigma if sigma else series * 0.0

    lo, hi = series.min(), series.max()
    return (series - lo) / (hi - lo) if hi > lo else series * 0.0


# --------------------------------------------------------------------------- #
# Internal metrics (lead time, vendor mix, inventory posture)
# --------------------------------------------------------------------------- #
def _internal_metrics(inv_path: Path, vendor_path: Path) -> pd.DataFrame:
    inv = load_vendor_inventory(inv_path)
    vendors = load_all_vendors(vendor_path)

    agg = inv.groupby("category_name").agg(
        avg_lead_time=("average_lead_time_(days)", "mean"),
        lead_time_sd=("standard_deviation_of_lead_time_(days)", "mean"),
        days_of_supply=("days_of_supply_(current)", "mean"),
    )

    total_vendors = vendors.groupby("category_name")["vendornumber_clean"].nunique()
    us_vendors = (
        vendors.loc[vendors["restrictedusvendor"] == "Y"]
        .groupby("category_name")["vendornumber_clean"]
        .nunique()
    )

    agg["vendor_concentration"] = 1 / total_vendors
    agg["us_dependency"] = us_vendors.div(total_vendors).fillna(0.0)

    # coefficient of variation
    agg["lead_time_cv"] = (
        agg["lead_time_sd"].div(agg["avg_lead_time"].replace({0: np.nan})).fillna(0.0)
    )

    # make scaled columns
    for raw in (
        "avg_lead_time",
        "lead_time_cv",
        "vendor_concentration",
        "days_of_supply",
    ):
        agg[f"scaled_{raw}"] = _scale(agg[raw], method=config.SCALING)

    return agg.reset_index()


# --------------------------------------------------------------------------- #
# External metrics (logistics, macro exposure)
# --------------------------------------------------------------------------- #
def _external_metrics(inv_path: Path, lpi_path: Path) -> pd.DataFrame:
    inv = load_vendor_inventory(inv_path)
    lpi = load_lpi(lpi_path)[["country_name", "lpi_score"]]

    merged = inv.merge(
        lpi, left_on="country_of_origin", right_on="country_name", how="left"
    )
    median_lpi: Final = lpi["lpi_score"].median()
    merged["lpi_score"] = merged["lpi_score"].fillna(median_lpi)

    g = (
        merged.groupby("category_name")["lpi_score"]
        .mean()
        .rename("avg_lpi")
        .reset_index()
    )
    g["scaled_logistics"] = 1 - _scale(g["avg_lpi"], method=config.SCALING)
    return g[["category_name", "scaled_logistics"]]


# --------------------------------------------------------------------------- #
# Public API
# --------------------------------------------------------------------------- #
def build_risk_table(
    inv_path: Path,
    vendor_path: Path,
    tol_path: Path,
    lpi_path: Path,
) -> pd.DataFrame:
    """Return a tidy DataFrame with all component and composite scores."""
    internal = _internal_metrics(inv_path, vendor_path)
    external = _external_metrics(inv_path, lpi_path)

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
    df["risk_tolerance"] = df["risk_tolerance"].fillna("Med")

    # ------------------------------------------------------------------ #
    # Composite calculations
    # ------------------------------------------------------------------ #
    df["internal_score"] = (
        df["scaled_avg_lead_time"] * config.INTERNAL_WEIGHTS["lead_time"]
        + df["scaled_lead_time_cv"] * config.INTERNAL_WEIGHTS["lead_time_cv"]
        + df["scaled_vendor_concentration"] * config.INTERNAL_WEIGHTS["vendor_concentration"]
        + df["scaled_days_of_supply"] * config.INTERNAL_WEIGHTS["days_of_supply"]
    )

    df["external_score"] = (
        df["scaled_logistics"] * config.EXTERNAL_WEIGHTS["logistics"]
        + df["us_dependency"] * config.EXTERNAL_WEIGHTS["us_dependency"]
    )

    df["base_risk_score"] = 0.5 * (df["internal_score"] + df["external_score"])

    df["adjusted_risk_score"] = (
        df["base_risk_score"]
        * df["risk_tolerance"].map(config.RISK_TOLERANCE_MULTIPLIER).fillna(0.85)
    )

    return df.sort_values("adjusted_risk_score", ascending=False).reset_index(drop=True)


# --------------------------------------------------------------------------- #
# Scenario helpers
# --------------------------------------------------------------------------- #
def apply_us_tariff_scenario(
    df: pd.DataFrame,
    *,
    add_pct: float = 25.0,
    dependency_threshold: float = 0.50,
    new_col: str = "scenario_risk_score",
) -> pd.DataFrame:
    """Return a copy of *df* with an extra scenario-specific risk column.

    Parameters
    ----------
    df : DataFrame returned by `build_risk_table`.
    add_pct : float
        Extra risk percentage applied (e.g., 25 for a 25 % duty).
    dependency_threshold : float
        Minimum US-dependency share required to trigger the bump.
    new_col : str
        Name of the column that will hold the scenario result.
    """
    bump = add_pct / 100.0
    out = df.copy()
    penalty = np.where(out["us_dependency"] >= dependency_threshold,
                       out["us_dependency"] * bump,
                       0.0)
    out[new_col] = out["adjusted_risk_score"] + penalty
    return out
