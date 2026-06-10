from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes.insight import router as insight_router
from routes.query import router as query_router
from routes.ml import router as ml_router
from routes.upload import router as upload_router

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
app.include_router(upload_router)


@app.get("/health")
def health_check():
    return {"status": "ok"}
