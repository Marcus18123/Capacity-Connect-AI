from pydantic import BaseModel, Field
from typing import List

class CompetencyMapping(BaseModel):
    extracted_skill: str = Field(..., description="The raw skill extracted from the profile.")
    matched_competency_id: str = Field(..., description="The UUID of the mapped competency, or 'UNMAPPED'.")
    competency_name: str = Field(..., description="The official name of the competency.")
    confidence: float = Field(..., description="Confidence score from 0.0 to 1.0 of the match correctness.")
    relationship: str = Field(..., description="One of: DIRECT, RELATED, PARTIAL, UNMAPPED.")
    reason: str = Field(..., description="Why this mapping was made.")

class CompetencyMappingResult(BaseModel):
    mappings: List[CompetencyMapping] = Field(default_factory=list, description="List of all mappings.")
