from fastapi import APIRouter
from pydantic import BaseModel

from agents.ml_agent import train_dataset_model

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


@router.post("/train", response_model=TrainResponse)
def train_model(request: TrainRequest):
    """Train AutoML models on a dataset retrieved from MongoDB."""
    result = train_dataset_model(
        dataset_id=request.dataset_id,
        target_column=request.target_column,
        test_size=request.test_size,
        random_state=request.random_state,
    )
    return TrainResponse(**result)
