from fastapi import APIRouter
from pydantic import BaseModel

from agents.insight_agent import generate_business_insights

router = APIRouter()


class InsightRequest(BaseModel):
    statistics: dict


class InsightResponse(BaseModel):
    prompt: str
    insights: str


@router.post("/insights", response_model=InsightResponse)
def create_insights(request: InsightRequest):
    """Generate business insights from dataframe statistics using Gemini."""
    result = generate_business_insights(request.statistics)
    return InsightResponse(**result)


class DatasetInsightRequest(BaseModel):
    dataset_id: str
    system_prompt: str | None = None


class DatasetInsightResponse(BaseModel):
    insight_id: str
    insights: str


@router.post("/insights/from_dataset", response_model=DatasetInsightResponse)
def insights_from_dataset(request: DatasetInsightRequest):
    """Fetch dataset by id, compute stats & correlations, call Gemini, save insight, return it."""
    import json

    from utils.db import get_dataset, save_insight
    from utils.stats import compute_missing_value_analysis
    from utils.ai import generate_insight_from_stats

    # Load dataset
    df = get_dataset(request.dataset_id)

    # Compute describe and correlation and missing-value analysis
    describe_json = json.loads(df.describe(include="all").to_json()) if not df.empty else {}
    corr_json = json.loads(df.corr().to_json()) if not df.empty else {}
    missing = compute_missing_value_analysis(df)

    stats = {
        "row_count": int(df.shape[0]),
        "column_count": int(df.shape[1]),
        "describe": describe_json,
        "corr": corr_json,
        "missing": missing,
    }

    # Call Gemini wrapper
    insights_text = generate_insight_from_stats(stats, system_prompt=request.system_prompt)

    # Persist the insight
    insight_id = save_insight(request.dataset_id, insights_text, metadata={"row_count": df.shape[0], "column_count": df.shape[1]})

    return DatasetInsightResponse(insight_id=insight_id, insights=insights_text)
