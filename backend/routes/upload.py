import sys
import traceback

print("Loading routes.upload...", file=sys.stderr)
try:
    from fastapi import APIRouter, UploadFile, File, HTTPException
    from pydantic import BaseModel
    from typing import List, Dict, Any
    import pandas as pd
    import numpy as np
    from io import StringIO
    import logging
    
    try:
        from logging_config import setup_logging
    except ImportError:
        import logging as fallback_logging
        setup_logging = lambda x: fallback_logging.getLogger(x)
    
    logger = setup_logging(__name__)
    router = APIRouter()
    print("✅ routes.upload loaded successfully", file=sys.stderr)
    
except Exception as e:
    print(f"❌ Failed to load routes.upload: {str(e)}", file=sys.stderr)
    print(traceback.format_exc(), file=sys.stderr)
    raise

class UploadResponse(BaseModel):
    status: str
    filename: str
    rows: int
    columns: int
    column_names: List[str]
    data: List[Dict[str, Any]]
    dtypes: Dict[str, str]

@router.post("/upload", response_model=UploadResponse)
async def upload_csv(file: UploadFile = File(...)) -> UploadResponse:
    """
    Upload and process a CSV file.
    
    Args:
        file: CSV file to upload
        
    Returns:
        UploadResponse with file metadata and preview data
    """
    try:
        logger.info(f"Processing upload for file: {file.filename}")
        
        if not file.filename.endswith(".csv"):
            logger.warning(f"Non-CSV file upload attempted: {file.filename}")
            raise HTTPException(status_code=400, detail="Only CSV files are allowed")
        
        contents = await file.read()
        df = pd.read_csv(StringIO(contents.decode("utf-8")))
        
        logger.info(f"CSV loaded: {len(df)} rows, {len(df.columns)} columns")
        
        df = df.replace([np.inf, -np.inf], None)
        df = df.where(pd.notnull(df), None)
        
        response = UploadResponse(
            status="success",
            filename=file.filename,
            rows=len(df),
            columns=len(df.columns),
            column_names=df.columns.tolist(),
            data=df.head(10).to_dict(orient="records"),
            dtypes={col: str(dtype) for col, dtype in df.dtypes.items()}
        )
        
        logger.info(f"Upload successful: {file.filename}")
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Upload failed: {str(e)}", exc_info=True)
        raise HTTPException(status_code=400, detail=str(e))
