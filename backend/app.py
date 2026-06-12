import sys
import traceback
import logging

# Setup logging FIRST before anything else
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

logger.info("=" * 60)
logger.info("🚀 FastAPI Backend Starting")
logger.info("=" * 60)

try:
    logger.info("Step 1: Importing FastAPI modules...")
    from fastapi import FastAPI
    from fastapi.middleware.cors import CORSMiddleware
    from contextlib import asynccontextmanager
    from typing import Dict, Any
    logger.info("✅ FastAPI modules imported")
except Exception as e:
    logger.error(f"❌ Failed to import FastAPI: {str(e)}")
    logger.error(traceback.format_exc())
    sys.exit(1)

try:
    logger.info("Step 2: Importing logging config...")
    from logging_config import setup_logging
    logger.info("✅ Logging config imported")
except Exception as e:
    logger.error(f"❌ Failed to import logging_config: {str(e)}")
    logger.error(traceback.format_exc())
    sys.exit(1)

try:
    logger.info("Step 3: Importing config...")
    import config
    logger.info(f"✅ Config imported (DEBUG={config.DEBUG})")
except Exception as e:
    logger.error(f"❌ Failed to import config: {str(e)}")
    logger.error(traceback.format_exc())
    sys.exit(1)

try:
    logger.info("Step 4: Importing routes...")
    from routes.upload import router as upload_router
    logger.info("✅ Upload router imported")
    
    from routes.insights import router as insights_router
    logger.info("✅ Insights router imported")
    
    from routes.query import router as query_router
    logger.info("✅ Query router imported")
    
    from routes.modeling import router as modeling_router
    logger.info("✅ Modeling router imported")
except Exception as e:
    logger.error(f"❌ Failed to import routes: {str(e)}")
    logger.error(traceback.format_exc())
    sys.exit(1)

try:
    logger.info("Step 5: Creating FastAPI app...")
    
    @asynccontextmanager
    async def lifespan(app: FastAPI):
        logger.info("✅ App startup complete")
        yield
        logger.info("🛑 App shutdown")
    
    app = FastAPI(
        title="Autonomous AI Data Analyst API",
        description="AI-powered data analysis platform",
        version="1.0.0",
        lifespan=lifespan
    )
    logger.info("✅ FastAPI app created")
except Exception as e:
    logger.error(f"❌ Failed to create FastAPI app: {str(e)}")
    logger.error(traceback.format_exc())
    sys.exit(1)

try:
    logger.info("Step 6: Adding CORS middleware...")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    logger.info("✅ CORS middleware added")
except Exception as e:
    logger.error(f"❌ Failed to add CORS: {str(e)}")
    logger.error(traceback.format_exc())
    sys.exit(1)

try:
    logger.info("Step 7: Registering routes...")
    app.include_router(upload_router, prefix="/api", tags=["Upload"])
    logger.info("✅ Upload router registered")
    
    app.include_router(insights_router, prefix="/api", tags=["Insights"])
    logger.info("✅ Insights router registered")
    
    app.include_router(query_router, prefix="/api", tags=["Query"])
    logger.info("✅ Query router registered")
    
    app.include_router(modeling_router, prefix="/api", tags=["Modeling"])
    logger.info("✅ Modeling router registered")
except Exception as e:
    logger.error(f"❌ Failed to register routes: {str(e)}")
    logger.error(traceback.format_exc())
    sys.exit(1)

try:
    logger.info("Step 8: Adding health check endpoint...")
    
    @app.get("/health")
    async def health_check() -> Dict[str, Any]:
        return {
            "status": "healthy",
            "version": "1.0.0",
            "debug": config.DEBUG
        }
    
    logger.info("✅ Health check endpoint added")
except Exception as e:
    logger.error(f"❌ Failed to add health check: {str(e)}")
    logger.error(traceback.format_exc())
    sys.exit(1)

try:
    logger.info("Step 9: Adding root endpoint...")
    
    @app.get("/")
    async def root() -> Dict[str, str]:
        return {
            "message": "Autonomous AI Data Analyst API",
            "docs": "/docs",
            "health": "/health"
        }
    
    logger.info("✅ Root endpoint added")
except Exception as e:
    logger.error(f"❌ Failed to add root endpoint: {str(e)}")
    logger.error(traceback.format_exc())
    sys.exit(1)

logger.info("=" * 60)
logger.info("✅ FastAPI Application initialized successfully!")
logger.info("=" * 60)

if __name__ == "__main__":
    import uvicorn
    try:
        logger.info("Starting uvicorn server...")
        uvicorn.run(
            app,
            host="0.0.0.0",
            port=8000,
            log_level=config.LOG_LEVEL.lower()
        )
    except Exception as e:
        logger.error(f"❌ Failed to start uvicorn: {str(e)}")
        logger.error(traceback.format_exc())
        sys.exit(1)
