import sys
import traceback

print("Loading routes.insights...", file=sys.stderr)
try:
    from fastapi import APIRouter, HTTPException
    from pydantic import BaseModel
    from typing import Optional
    import google.generativeai as genai
    import logging
    
    try:
        from logging_config import setup_logging
    except ImportError:
        import logging as fallback_logging
        setup_logging = lambda x: fallback_logging.getLogger(x)
    import config
    
    logger = setup_logging(__name__)
    router = APIRouter()
    print("✅ routes.insights loaded successfully", file=sys.stderr)
    
except Exception as e:
    print(f"❌ Failed to load routes.insights: {str(e)}", file=sys.stderr)
    print(traceback.format_exc(), file=sys.stderr)
    raise

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
