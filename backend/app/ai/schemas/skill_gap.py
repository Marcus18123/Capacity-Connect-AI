from pydantic import BaseModel, Field
from typing import List

class GapReasoning(BaseModel):
    competency_id: str
    competency_name: str
    gap_levels: float = Field(..., description="Numerical difference between required and current level.")
    priority: str = Field(..., description="LOW, MEDIUM, HIGH, or CRITICAL.")
    priority_reason: str = Field(..., description="Explain why this priority was assigned.")

class SkillGapAnalysisResult(BaseModel):
    target_role: str
    overall_alignment_percentage: float
    gaps: List[GapReasoning] = Field(default_factory=list)
