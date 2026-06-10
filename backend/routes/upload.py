from fastapi import APIRouter, UploadFile, File, HTTPException
import pandas as pd
import numpy as np
from io import StringIO

router = APIRouter()

@router.post("/upload")
async def upload_csv(file: UploadFile = File(...)):
    """Upload and process CSV file."""
    if not file.filename.lower().endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only CSV files allowed")

    contents = await file.read()
    try:
        csv_text = contents.decode("utf-8-sig")
        df = pd.read_csv(StringIO(csv_text))
    except Exception as exc:
        raise HTTPException(status_code=400, detail=f"Unable to parse CSV: {exc}")

    df = df.replace([np.inf, -np.inf], None)
    df = df.where(pd.notnull(df), None)

    return {
        "filename": file.filename,
        "rows": len(df),
        "columns": len(df.columns),
        "column_names": df.columns.tolist(),
        "data": df.to_dict(orient="records"),
        "dtypes": df.dtypes.astype(str).to_dict(),
    }
