from typing import List, Dict

import numpy as np
import pandas as pd
from fastapi import FastAPI

from routes.insight import router as insight_router
from routes.query import router as query_router
from routes.ml import router as ml_router
from utils.json_utils import clean_dataframe_nan

app = FastAPI(
    title="Autonomous AI Data Analyst Platform Backend",
    description="Backend for generating business insights, data query and AutoML workflows.",
)

app.include_router(insight_router, prefix="/api")
app.include_router(query_router, prefix="/api")
app.include_router(ml_router, prefix="/api")


@app.get("/health")
def health_check():
    return {"status": "ok"}


# ISSUE 3 FIX: Clean NaN/inf values from JSON data using utility function
@app.post("/upload")
async def upload_data(payload: List[Dict]):
    """Receive uploaded CSV data as JSON list of records.

    This endpoint accepts an array of objects representing rows (e.g. `df.to_dict(orient='records')`).
    Currently it returns the number of records received; implement persistence or further processing later.
    
    NaN and inf values are automatically cleaned to ensure JSON serialization succeeds.
    """
    # Convert to DataFrame to clean NaN/inf values
    df = pd.DataFrame(payload)
    
    # Clean NaN and inf values using utility function
    df_clean = clean_dataframe_nan(df)
    
    # Convert back to records
    cleaned_records = df_clean.to_dict(orient="records")
    
    return {
        "received": len(cleaned_records),
        "data": cleaned_records,
        "status": "success",
        "message": "CSV data uploaded and cleaned successfully"
    }
