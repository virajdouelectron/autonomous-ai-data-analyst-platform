from typing import List, Dict

from fastapi import FastAPI

from routes.insight import router as insight_router

app = FastAPI(
    title="Autonomous AI Data Analyst Platform Backend",
    description="Backend for generating business insights from dataframe statistics using Gemini API.",
)

app.include_router(insight_router, prefix="/api")


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/upload")
async def upload_data(payload: List[Dict]):
    """Receive uploaded CSV data as JSON list of records.

    This endpoint accepts an array of objects representing rows (e.g. `df.to_dict(orient='records')`).
    Currently it returns the number of records received; implement persistence or further processing later.
    """
    return {"received": len(payload)}
