from fastapi import APIRouter, UploadFile, File
from fastapi.responses import JSONResponse
import pandas as pd
from io import StringIO

router = APIRouter()


@router.post("/upload")
async def upload_csv(file: UploadFile = File(...)):
    if not file.filename.endswith(".csv"):
        return JSONResponse(
            status_code=400,
            content={"error": "Only CSV files allowed"}
        )

    contents = await file.read()
    df = pd.read_csv(StringIO(contents.decode("utf-8")))

    # Handle NaN values
    df = df.where(pd.notnull(df), None)

    return {
        "filename": file.filename,
        "rows": len(df),
        "columns": len(df.columns),
        "column_names": df.columns.tolist(),
        "data": df.to_dict(orient="records")
    }