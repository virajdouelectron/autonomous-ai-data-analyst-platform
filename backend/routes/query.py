from typing import Dict

from fastapi import APIRouter
from pydantic import BaseModel

from agents.query_agent import generate_pandas_code, query_dataset
from utils.db import save_query_history

router = APIRouter()


class QueryRequest(BaseModel):
    question: str
    schema: Dict[str, str]


class QueryResponse(BaseModel):
    prompt: str
    pandas_code: str


class DatasetQueryRequest(BaseModel):
    dataset_id: str
    question: str


class DatasetQueryResponse(BaseModel):
    prompt: str
    pandas_code: str
    result: dict | None
    error: str | None = None


@router.post("/query", response_model=QueryResponse)
def create_query_code(request: QueryRequest):
    """Generate valid pandas code for a user's natural language question."""
    result = generate_pandas_code(request.question, request.schema)
    save_query_history(
        question=request.question,
        pandas_code=result["pandas_code"],
        schema=request.schema,
    )
    return QueryResponse(**result)


@router.post("/query/dataset", response_model=DatasetQueryResponse)
def create_dataset_query(request: DatasetQueryRequest):
    """Generate pandas code from a question and execute it against a dataset stored in MongoDB."""
    result = query_dataset(request.dataset_id, request.question)
    save_query_history(
        question=request.question,
        pandas_code=result["pandas_code"],
        schema="dataset_id: " + request.dataset_id,
        dataset_id=request.dataset_id,
    )
    return DatasetQueryResponse(**result)
