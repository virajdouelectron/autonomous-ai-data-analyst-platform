import sys
import traceback

print("Loading routes.query...", file=sys.stderr)
try:
    from fastapi import APIRouter, HTTPException
    from pydantic import BaseModel
    from typing import List
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
    print("✅ routes.query loaded successfully", file=sys.stderr)
    
except Exception as e:
    print(f"❌ Failed to load routes.query: {str(e)}", file=sys.stderr)
    print(traceback.format_exc(), file=sys.stderr)
    raise

if config.GEMINI_API_KEY:
    genai.configure(api_key=config.GEMINI_API_KEY)

class QueryRequest(BaseModel):
    question: str
    column_names: List[str]

class QueryResponse(BaseModel):
    status: str
    code: str

@router.post("/query", response_model=QueryResponse)
async def generate_query(request: QueryRequest) -> QueryResponse:
    """
    Generate pandas code from natural language query.
    
    Args:
        request: QueryRequest with question and column names
        
    Returns:
        QueryResponse with generated pandas code
    """
    try:
        if not config.GEMINI_API_KEY:
            logger.warning("Gemini API key not configured")
            return QueryResponse(
                status="warning",
                code="# Gemini API not configured"
            )
        
        logger.info(f"Generating query for: {request.question[:50]}...")
        
        model = genai.GenerativeModel('gemini-pro')
        prompt = f"""Given a pandas DataFrame with columns: {request.column_names}

User question: {request.question}

Generate ONLY valid pandas code (no explanations, no markdown).
Return executable code that answers the question.
Start with: df = df[...]"""
        
        response = model.generate_content(prompt)
        
        logger.info("Query generated successfully")
        return QueryResponse(
            status="success",
            code=response.text
        )
        
    except Exception as e:
        logger.error(f"Query generation failed: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))
