"""Utility functions for JSON serialization and data cleaning."""
import numpy as np
import pandas as pd
from typing import Any, Dict, List


def clean_dataframe_nan(df: pd.DataFrame) -> pd.DataFrame:
    """Replace NaN and inf values in DataFrame with None for JSON serialization.
    
    Args:
        df: Input DataFrame
        
    Returns:
        DataFrame with NaN and inf values replaced with None
    """
    df = df.copy()
    # Replace inf and -inf with None
    df = df.replace([np.inf, -np.inf], None)
    # Replace NaN with None
    df = df.where(pd.notnull(df), None)
    return df


def _clean_list_nan(lst: List[Any]) -> List[Any]:
    """Recursively replace NaN and inf values in a list with None."""
    cleaned_lst = []
    for v in lst:
        if isinstance(v, float):
            if np.isnan(v) or np.isinf(v):
                cleaned_lst.append(None)
            else:
                cleaned_lst.append(v)
        elif isinstance(v, dict):
            cleaned_lst.append(clean_dict_nan(v))
        elif isinstance(v, list):
            cleaned_lst.append(_clean_list_nan(v))
        else:
            cleaned_lst.append(v)
    return cleaned_lst


def clean_dict_nan(data: Dict[str, Any]) -> Dict[str, Any]:
    """Replace NaN and inf values in dict with None for JSON serialization.
    
    Args:
        data: Input dictionary
        
    Returns:
        Dictionary with NaN and inf values replaced with None
    """
    cleaned = {}
    for key, value in data.items():
        if isinstance(value, float):
            if np.isnan(value) or np.isinf(value):
                cleaned[key] = None
            else:
                cleaned[key] = value
        elif isinstance(value, dict):
            cleaned[key] = clean_dict_nan(value)
        elif isinstance(value, list):
            cleaned[key] = _clean_list_nan(value)
        else:
            cleaned[key] = value
    return cleaned


def convert_dataframe_to_json_serializable(df: pd.DataFrame, orient: str = "records") -> Any:
    """Convert DataFrame to JSON-serializable format.
    
    Args:
        df: Input DataFrame
        orient: Orientation for to_dict() method
        
    Returns:
        JSON-serializable data (dict or list of dicts)
    """
    df_clean = clean_dataframe_nan(df)
    return df_clean.to_dict(orient=orient)
