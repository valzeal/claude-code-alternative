"""
Claude Code Alternative - API Framework
FastAPI-based REST API for the code assistant
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, List, Optional
import uvicorn

# Import NLP processor
from nlp_module.nlp_processor import NLPProcessor

app = FastAPI(
    title="Claude Code Alternative API",
    description="API for code generation and analysis assistant",
    version="1.0.0"
)

# Initialize NLP processor
nlp_processor = NLPProcessor()

class CodeRequest(BaseModel):
    text: str
    language: Optional[str] = None
    request_type: Optional[str] = None

class CodeAnalysisRequest(BaseModel):
    code: str
    language: str

class CodeResponse(BaseModel):
    request_type: str
    confidence: float
    keywords: List[str]
    language: Optional[str] = None
    functions: List[str] = []
    analysis: Optional[Dict] = None

@app.get("/")
def root():
    """Health check endpoint"""
    return {"status": "running", "service": "Claude Code Alternative API"}

@app.post("/analyze", response_model=CodeResponse)
def analyze_code_request(request: CodeRequest):
    """Analyze a code-related request"""
    try:
        # Parse and analyze the request
        analysis = nlp_processor.extract_code_requirements(request.text)
        
        return CodeResponse(
            request_type=analysis["request_type"],
            confidence=analysis["confidence"],
            keywords=analysis["keywords"],
            language=analysis.get("language"),
            functions=analysis.get("functions", []),
            analysis=analysis
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

@app.post("/generate")
def generate_code(request: CodeRequest):
    """Generate code based on request (placeholder)"""
    try:
        # This would integrate with code generation engine
        analysis = nlp_processor.extract_code_requirements(request.text)
        
        return {
            "status": "pending",
            "request_type": analysis["request_type"],
            "language": analysis.get("language"),
            "functions": analysis.get("functions", []),
            "message": "Code generation in progress..."
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Generation failed: {str(e)}")

@app.post("/review")
def review_code(request: CodeAnalysisRequest):
    """Review and analyze code (placeholder)"""
    try:
        # This would integrate with code analysis engine
        return {
            "status": "pending",
            "language": request.language,
            "code_length": len(request.code),
            "message": "Code review in progress..."
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Review failed: {str(e)}")

@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "Claude Code Alternative API",
        "nlp_initialized": nlp_processor is not None
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)