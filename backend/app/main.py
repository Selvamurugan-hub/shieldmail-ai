from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from . import analyzer
from .config import CORS_ORIGINS, MAX_CHARS
from .examples import EXAMPLES
from .schemas import AnalyzeRequest, AnalyzeResponse

app = FastAPI(title="ShieldMail AI", version="0.1.0")
app.add_middleware(CORSMiddleware, allow_origins=CORS_ORIGINS, allow_methods=["GET", "POST"], allow_headers=["*"])

@app.get("/api/health")
def health():
    return {"status": "ok", "analysis_mode": "Rule-based", "model_configured": False, "max_chars": MAX_CHARS}

@app.get("/api/examples")
def examples():
    return EXAMPLES

@app.post("/api/analyze", response_model=AnalyzeResponse)
def analyze(req: AnalyzeRequest):
    if len(req.message) > MAX_CHARS:
        raise HTTPException(status_code=413, detail=f"Message exceeds {MAX_CHARS} characters.")
    return analyzer.analyze(req.message, req.sender, req.url, req.message_type)
