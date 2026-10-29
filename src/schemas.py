from pydantic import BaseModel, Field, ConfigDict
from typing import Literal

class CustomerInsight(BaseModel):
    model_config = ConfigDict(extra="forbid")
    customer_summary: str = Field(min_length=5, max_length=500)
    risk_level: Literal["low", "medium", "high"]
    recommended_action: str = Field(min_length=5, max_length=300)
    confidence: float = Field(ge=0.0, le=1.0)
    evidence_note: str = Field(min_length=3, max_length=300)
