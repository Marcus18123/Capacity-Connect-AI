from pydantic import BaseModel, Field
from typing import List

class LearningRecommendation(BaseModel):
    course_id: str
    course_title: str
    target_competency_id: str
    reason: str = Field(..., description="Why this course is recommended for this gap.")
    priority: int = Field(..., description="Order of recommendation (1 is first).")
    estimated_duration_hours: float
    prerequisites_met: bool = Field(..., description="Are all prerequisites for this course met?")

class LearningPathResult(BaseModel):
    target_role: str
    recommendations: List[LearningRecommendation] = Field(default_factory=list)
