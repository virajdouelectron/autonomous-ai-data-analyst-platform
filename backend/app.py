from typing import Dict

import numpy as np
import pandas as pd
from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware

from routes.insight import router as insight_router
from routes.query import router as query_router
from routes.ml import router as ml_router
from utils.json_utils import clean_dataframe_nan

app = FastAPI(
    title="Autonomous AI Data Analyst Platform Backend",
    description="Backend for generating business insights, data query and AutoML workflows.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(insight_router, prefix="/api")
app.include_router(query_router, prefix="/api")
app.include_router(ml_router, prefix="/api")


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/upload")
async def upload_data(file: UploadFile = File(...)):
    """Receive an uploaded CSV file, clean it, and return preview records.

    The frontend sends the file as multipart/form-data directly to FastAPI so
    Hugging Face's file handler does not intercept the upload.
    """
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file name provided")

    try:
        df = pd.read_csv(file.file)
    except Exception as exc:
        raise HTTPException(status_code=400, detail=f"Unable to parse CSV file: {exc}") from exc

    df_clean = clean_dataframe_nan(df)
    cleaned_records = df_clean.to_dict(orient="records")

    return {
        "received": len(cleaned_records),
        "data": cleaned_records,
        "status": "success",
        "message": "CSV data uploaded and cleaned successfully",
    }
