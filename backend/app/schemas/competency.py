from pydantic import BaseModel
from typing import Optional, List
from uuid import UUID
from datetime import datetime
from app.models.competency import CompetencyLevel
from app.models.user_competency import VerificationStatus

class CompetencyBase(BaseModel):
    name: str
    description: Optional[str] = None
    category: Optional[str] = None
    level: CompetencyLevel
    parent_id: Optional[UUID] = None

class CompetencyCreate(CompetencyBase):
    pass

class CompetencyResponse(CompetencyBase):
    id: UUID
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

class UserCompetencyBase(BaseModel):
    competency_id: UUID
    proficiency_level: float
    confidence: float
    evidence_url: Optional[str] = None

class UserCompetencyResponse(UserCompetencyBase):
    id: UUID
    user_id: UUID
    verification_status: VerificationStatus
    last_assessed_at: Optional[datetime] = None
    competency: Optional[CompetencyResponse] = None

    class Config:
        from_attributes = True
