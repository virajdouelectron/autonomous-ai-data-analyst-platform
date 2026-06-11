from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from typing import Dict, Any
import logging

from logging_config import setup_logging
import config
from routes.upload import router as upload_router
from routes.insights import router as insights_router
from routes.query import router as query_router
from routes.modeling import router as modeling_router

logger = setup_logging(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifecycle management."""
    logger.info("🚀 FastAPI Application Starting")
    logger.info(f"DEBUG Mode: {config.DEBUG}")
    logger.info(f"Log Level: {config.LOG_LEVEL}")
    yield
    logger.info("🛑 FastAPI Application Shutting Down")

app = FastAPI(
    title="Autonomous AI Data Analyst API",
    description="AI-powered data analysis platform",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(upload_router, prefix="/api", tags=["Upload"])
app.include_router(insights_router, prefix="/api", tags=["Insights"])
app.include_router(query_router, prefix="/api", tags=["Query"])
app.include_router(modeling_router, prefix="/api", tags=["Modeling"])

@app.get("/health", tags=["Health"])
async def health_check() -> Dict[str, Any]:
    """Health check endpoint for monitoring."""
    return {
        "status": "healthy",
        "version": "1.0.0",
        "debug": config.DEBUG
    }

@app.get("/", tags=["Root"])
async def root() -> Dict[str, str]:
    """Root endpoint with API information."""
    return {
        "message": "Autonomous AI Data Analyst API",
        "docs": "/docs",
        "health": "/health"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level=config.LOG_LEVEL.lower()
    )
