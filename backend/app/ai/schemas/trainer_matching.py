from pydantic import BaseModel, Field
from typing import List

class TrainerMatchReason(BaseModel):
    competency_overlap: float = Field(..., description="Percentage of competency overlap.")
    experience_relevance: float = Field(..., description="Percentage relevance of experience.")
    domain_relevance: float = Field(..., description="Percentage relevance of industry/domain.")
    availability_score: float = Field(..., description="Score based on availability matching.")
    summary: str = Field(..., description="Natural language explanation of why this trainer is a good match.")

class TrainerMatch(BaseModel):
    trainer_id: str
    trainer_name: str
    overall_match_score: float = Field(..., description="Overall match out of 100.")
    matched_competencies: List[str]
    reasons: TrainerMatchReason

class TrainerMatchingResult(BaseModel):
    trainee_id: str
    matches: List[TrainerMatch] = Field(default_factory=list)
