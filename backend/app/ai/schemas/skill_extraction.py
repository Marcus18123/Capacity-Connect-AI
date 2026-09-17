from pydantic import BaseModel, Field
from typing import List, Optional

class ExtractedSkill(BaseModel):
    name: str = Field(..., description="The name of the skill extracted.")
    evidence: str = Field(..., description="The exact text snippet where this skill was found.")
    confidence: float = Field(..., description="Confidence score from 0.0 to 1.0 that this skill is genuinely possessed.")
    type: str = Field(..., description="Type of skill: TECHNICAL, DOMAIN, TOOL, METHODOLOGY, or SOFT.")
    years_experience: Optional[float] = Field(None, description="Years of experience if explicitly stated, otherwise null.")

class SkillExtractionResult(BaseModel):
    skills: List[ExtractedSkill] = Field(default_factory=list, description="List of all extracted skills.")
