from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
import google.generativeai as genai
import logging

try:
    from logging_config import setup_logging
except ImportError:
    import logging
    logging.basicConfig(level=logging.INFO)
    setup_logging = logging.getLogger
import config

logger = setup_logging(__name__)
router = APIRouter()

if config.GEMINI_API_KEY:
    genai.configure(api_key=config.GEMINI_API_KEY)

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
        if not config.GEMINI_API_KEY:
            logger.warning("Gemini API key not configured")
            return InsightResponse(
                status="warning",
                insights="Gemini API not configured. Please set GEMINI_API_KEY."
            )
        
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
