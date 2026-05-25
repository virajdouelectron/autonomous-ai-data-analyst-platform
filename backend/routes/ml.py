from fastapi import APIRouter
from pydantic import BaseModel

import numpy as np

from agents.ml_agent import train_dataset_model
from utils.json_utils import clean_dict_nan

router = APIRouter()


class TrainRequest(BaseModel):
    dataset_id: str
    target_column: str
    test_size: float = 0.2
    random_state: int = 42


class TrainResponse(BaseModel):
    dataset_id: str
    target_column: str
    problem_type: str
    best_model: str
    best_model_metrics: dict
    best_model_feature_importance: dict | None = None
    candidate_models: dict
    feature_columns: list[str]
    row_count: int
    column_count: int


# ISSUE 3 FIX: Clean NaN/inf values from metrics and feature importance dicts
@router.post("/train", response_model=TrainResponse)
def train_model(request: TrainRequest):
    """Train AutoML models on a dataset retrieved from MongoDB."""
    result = train_dataset_model(
        dataset_id=request.dataset_id,
        target_column=request.target_column,
        test_size=request.test_size,
        random_state=request.random_state,
    )
    
    # ISSUE 3 FIX: Clean NaN/inf values using utility function
    result["best_model_metrics"] = clean_dict_nan(result["best_model_metrics"])
    
    if result.get("best_model_feature_importance"):
        result["best_model_feature_importance"] = clean_dict_nan(result["best_model_feature_importance"])
    
    # ISSUE 3 FIX: Clean all candidate model metrics
    for model_name, model_data in result.get("candidate_models", {}).items():
        if isinstance(model_data, dict) and "metrics" in model_data:
            model_data["metrics"] = clean_dict_nan(model_data["metrics"])
        if isinstance(model_data, dict) and "feature_importance" in model_data and model_data["feature_importance"]:
            model_data["feature_importance"] = clean_dict_nan(model_data["feature_importance"])
    
    return TrainResponse(**result)
