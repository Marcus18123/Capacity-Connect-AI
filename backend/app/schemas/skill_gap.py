from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from datetime import datetime
from app.models.competency import CompetencyLevel
from app.models.learning_path_item import Priority
from app.models.skill_gap import SkillGapStatus

class SkillGapBase(BaseModel):
    competency_id: UUID
    current_level: CompetencyLevel
    target_level: CompetencyLevel
    gap_percentage: float
    priority: Priority
    reason: Optional[str] = None

class SkillGapResponse(SkillGapBase):
    id: UUID
    trainee_id: UUID
    status: SkillGapStatus
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
