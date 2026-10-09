from typing import Literal, Optional
from pydantic import BaseModel, Field, field_validator

class AnalyzeRequest(BaseModel):
    message: str
    message_type: Literal["email", "sms", "other"] = "email"
    sender: Optional[str] = Field(default=None, max_length=320)
    url: Optional[str] = Field(default=None, max_length=2048)

    @field_validator("message")
    @classmethod
    def not_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Message must not be empty.")
        return v

class Finding(BaseModel):
    rule_id: str
    category: str
    title: str
    description: str
    severity: Literal["low", "medium", "high"]
    evidence: str
    points_contributed: int = 0

class AnalyzeResponse(BaseModel):
    analysis_id: str
    risk_score: int = Field(ge=0, le=100)
    risk_level: Literal["Low", "Medium", "High", "Critical"]
    verdict: str
    evidence_strength: str
    findings: list[Finding]
    evidence_snippets: list[str]
    recommendations: list[str]
    analysis_mode: str
    limitations: list[str]
    model_status: dict
