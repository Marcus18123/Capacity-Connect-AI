from pydantic import BaseModel
from typing import Optional, List
from uuid import UUID
from datetime import datetime
from app.models.learning_path import LearningPathStatus, GenerationMethod
from app.models.learning_path_item import PathItemStatus, Priority

class LearningPathItemBase(BaseModel):
    course_id: Optional[UUID] = None
    competency_id: Optional[UUID] = None
    sequence: int
    priority: Priority

class LearningPathItemResponse(LearningPathItemBase):
    id: UUID
    learning_path_id: UUID
    status: PathItemStatus
    progress_percentage: float
    
    class Config:
        from_attributes = True

class LearningPathBase(BaseModel):
    target_role: str
    current_alignment: float = 0.0

class LearningPathResponse(LearningPathBase):
    id: UUID
    trainee_id: UUID
    status: LearningPathStatus
    generated_by: GenerationMethod
    created_at: datetime
    updated_at: datetime
    
    items: Optional[List[LearningPathItemResponse]] = None

    class Config:
        from_attributes = True
