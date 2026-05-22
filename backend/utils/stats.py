"""
Utility functions for dataframe statistics and missing value analysis.

Provides a single helper `compute_missing_value_analysis` that accepts a
Pandas DataFrame and returns a JSON-serializable dict with per-column
information: missing count, missing percentage, dtype, and basic stats
(min, max, mean) for numeric columns.

Do not add persistence here; this is a pure analysis utility.
"""
from typing import Any, Dict

import pandas as pd
from pandas.api import types as pd_types


def compute_missing_value_analysis(df: pd.DataFrame) -> Dict[str, Dict[str, Any]]:
    """Compute missing-value summary and basic stats for each column.

    Returns a dict keyed by column name with values containing:
      - dtype: string representation of the column dtype
      - missing_count: int
      - missing_pct: float (percentage, rounded to 2 decimals)
      - min: minimum value for numeric columns (or None)
      - max: maximum value for numeric columns (or None)
      - mean: mean value for numeric columns (or None)

    All values are JSON-serializable (numbers, strings, or None).
    """
    results: Dict[str, Dict[str, Any]] = {}
    total_rows = len(df)

    for col in df.columns:
        series = df[col]
        dtype = str(series.dtype)
        missing_count = int(series.isna().sum())
        missing_pct = round((missing_count / total_rows * 100) if total_rows > 0 else 0.0, 2)

        col_min = None
        col_max = None
        col_mean = None

        # Numeric columns: compute min/max/mean as floats when possible
        if pd_types.is_numeric_dtype(series):
            try:
                cleaned = pd.to_numeric(series.dropna())
                if not cleaned.empty:
                    col_min = float(cleaned.min())
                    col_max = float(cleaned.max())
                    col_mean = float(round(cleaned.mean(), 6))
            except Exception:
                # If conversion fails, leave stats as None
                col_min = col_max = col_mean = None

        # For datetime columns, report min/max as ISO strings
        elif pd_types.is_datetime64_any_dtype(series):
            try:
                cleaned = pd.to_datetime(series.dropna(), errors="coerce").dropna()
                if not cleaned.empty:
                    col_min = cleaned.min().isoformat()
                    col_max = cleaned.max().isoformat()
            except Exception:
                col_min = col_max = None

        results[col] = {
            "dtype": dtype,
            "missing_count": missing_count,
            "missing_pct": missing_pct,
            "min": col_min,
            "max": col_max,
            "mean": col_mean,
        }

    return results
