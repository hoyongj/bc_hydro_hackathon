# config.py
# -----------------------------------------------------------------------------
# All weights, scalers and scenario knobs live here so you can tune them freely
# -----------------------------------------------------------------------------

INTERNAL_WEIGHTS = {
    "lead_time": 0.40,
    "lead_time_cv": 0.20,
    "vendor_concentration": 0.20,
    "days_of_supply": 0.20,
}

EXTERNAL_WEIGHTS = {
    "logistics": 0.50,
    "us_dependency": 0.30,
    "tariff": 0.20,          # placeholder – ready if you map HS-codes later
}

SCALING = "minmax"          # or "zscore"

# optional: map qualitative vendor-score text to a number
VENDOR_PERF_MAP = {"Poor": 1, "Average": 2, "Good": 3, "Excellent": 4}

RISK_TOLERANCE_MULTIPLIER = {"High": 1.00, "Med": 0.85, "Low": 0.70}

SCENARIOS = {
    "base": {"us_tariff_additional_pct": 0.0},
    "us_tariff_25pct": {"us_tariff_additional_pct": 25.0},
}
