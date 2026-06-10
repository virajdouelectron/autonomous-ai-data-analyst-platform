from typing import Dict, Any

from fastapi import APIRouter
from pydantic import BaseModel

import numpy as np
import pandas as pd

from agents.query_agent import generate_pandas_code, query_dataset
from utils.db import save_query_history
from utils.json_utils import clean_dataframe_nan, clean_dict_nan

router = APIRouter()


class QueryRequest(BaseModel):
    question: str
    schema_info: dict  # Renamed from 'schema'


class QueryResponse(BaseModel):
    prompt: str
    pandas_code: str


class DatasetQueryRequest(BaseModel):
    dataset_id: str
    question: str


class DatasetQueryResponse(BaseModel):
    prompt: str
    pandas_code: str
    result: list[dict] | dict | int | float | str | bool | None
    error: str | None = None


# ISSUE 3 FIX: Convert query results to JSON-serializable format using utility functions
def make_result_json_serializable(result: Any) -> list[dict] | dict | int | float | str | bool | None:
    """Convert query results to JSON-serializable format, replacing NaN/inf with None."""
    if result is None:
        return None
    
    if isinstance(result, pd.DataFrame):
        # Use utility function to clean NaN/inf values
        df_clean = clean_dataframe_nan(result)
        return df_clean.to_dict(orient="records")
    
    if isinstance(result, pd.Series):
        # Clean NaN/inf values in Series
        df = result.to_frame()
        df_clean = clean_dataframe_nan(df)
        return df_clean.to_dict(orient="records")
    
    if isinstance(result, dict):
        # Use utility function to clean dict values
        return clean_dict_nan(result)
    
    if isinstance(result, (int, float, str, bool)):
        if isinstance(result, float):
            import math
            return result if math.isfinite(result) else None
        return result
    
    return None


@router.post("/query", response_model=QueryResponse)
def create_query_code(request: QueryRequest):
    """Generate valid pandas code for a user's natural language question."""
    result = generate_pandas_code(request.question, request.schema_info)
    save_query_history(
        question=request.question,
        pandas_code=result["pandas_code"],
        schema=request.schema_info,
    )
    return QueryResponse(**result)


@router.post("/query/dataset", response_model=DatasetQueryResponse)
def create_dataset_query(request: DatasetQueryRequest):
    """Generate pandas code from a question and execute it against a dataset stored in MongoDB."""
    result = query_dataset(request.dataset_id, request.question)
    
    # ISSUE 3 FIX: Make result JSON-serializable by replacing NaN/inf with None
    if result.get("result") is not None:
        result["result"] = make_result_json_serializable(result["result"])
    
    save_query_history(
        question=request.question,
        pandas_code=result["pandas_code"],
        schema="dataset_id: " + request.dataset_id,
        dataset_id=request.dataset_id,
    )
    return DatasetQueryResponse(**result)
