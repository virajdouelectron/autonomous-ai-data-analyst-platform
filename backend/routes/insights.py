from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
import os
import logging

try:
    from logging_config import setup_logging
except ImportError:
    import logging as fallback_logging
    setup_logging = lambda x: fallback_logging.getLogger(x)

logger = setup_logging(__name__)
router = APIRouter()

try:
    import google.generativeai as genai
except ImportError:
    genai = None
    logger.warning("google-generativeai not installed, AI features disabled")

class InsightRequest(BaseModel):
    data_summary: str
    prompt: str

class InsightResponse(BaseModel):
    status: str
    insights: str

@router.post("/insights", response_model=InsightResponse)
async def generate_insights(request: InsightRequest) -> InsightResponse:
    """
    Generate AI-powered insights from data.
    
    Args:
        request: InsightRequest with data summary and prompt
        
    Returns:
        InsightResponse with generated insights
    """
    try:
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key or genai is None:
            logger.warning("Gemini API key not configured or package not installed")
            return InsightResponse(
                status="warning",
                insights="Gemini API not configured. Please set GEMINI_API_KEY."
            )

        genai.configure(api_key=api_key)
        logger.info("Generating insights with Gemini")

        model = genai.GenerativeModel('gemini-pro')
        full_prompt = f"""Dataset Summary:
{request.data_summary}

User Request:
{request.prompt}

Provide concise, actionable insights based on the data."""
        
        response = model.generate_content(full_prompt)
        
        logger.info("Insights generated successfully")
        return InsightResponse(
            status="success",
            insights=response.text
        )
        
    except Exception as e:
        logger.error(f"Insights generation failed: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))
