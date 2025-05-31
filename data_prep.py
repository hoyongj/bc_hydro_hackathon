# data_prep.py
"""Loader / cleaner helpers for every raw Excel file."""
import pandas as pd
from pathlib import Path

def _clean_columns(df: pd.DataFrame) -> pd.DataFrame:
    df.columns = [str(c).strip().lower().replace(" ", "_") for c in df.columns]
    return df

def load_vendor_inventory(path: Path) -> pd.DataFrame:
    return _clean_columns(pd.read_excel(path))

def load_all_vendors(path: Path) -> pd.DataFrame:
    return _clean_columns(pd.read_excel(path))

def load_risk_tolerance(path: Path) -> pd.DataFrame:
    return _clean_columns(pd.read_excel(path))

def load_lpi(path: Path) -> pd.DataFrame:
    return _clean_columns(pd.read_excel(path))

# (Tariff, Imports, Doing-Business loaders are ready when you want them)
