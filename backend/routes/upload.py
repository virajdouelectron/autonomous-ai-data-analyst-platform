from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import pandas as pd
import numpy as np
from io import StringIO

router = APIRouter()

@router.post("/upload")
async def upload_csv(file: UploadFile = File(...)):
    """Upload and process CSV file."""
    try:
        if not file.filename.endswith(".csv"):
            raise HTTPException(status_code=400, 
                              detail="Only CSV files allowed")
        
        contents = await file.read()
        df = pd.read_csv(StringIO(contents.decode("utf-8")))
        
        # Handle NaN/inf values
        df = df.replace([np.inf, -np.inf], None)
        df = df.where(pd.notnull(df), None)
        
        return {
            "filename": file.filename,
            "rows": len(df),
            "columns": len(df.columns),
            "column_names": df.columns.tolist(),
            "data": df.to_dict(orient="records"),
            "dtypes": df.dtypes.astype(str).to_dict()
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))