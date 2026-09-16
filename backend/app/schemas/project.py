from pydantic import BaseModel
from typing import Optional, List
from uuid import UUID
from datetime import datetime
from app.models.submission import SubmissionStatus

class ProjectBase(BaseModel):
    title: str
    description: Optional[str] = None
    instructions: Optional[str] = None
    rubric: Optional[str] = None
    deadline: Optional[datetime] = None

class ProjectResponse(ProjectBase):
    id: UUID
    course_id: Optional[UUID] = None
    created_by: Optional[UUID] = None
    created_at: datetime
    
    class Config:
        from_attributes = True

class SubmissionBase(BaseModel):
    submission_url: Optional[str] = None
    submission_text: Optional[str] = None

class SubmissionResponse(SubmissionBase):
    id: UUID
    project_id: UUID
    trainee_id: UUID
    score: Optional[int] = None
    feedback: Optional[str] = None
    status: SubmissionStatus
    submitted_at: datetime
    evaluated_at: Optional[datetime] = None
    evaluated_by: Optional[UUID] = None

    class Config:
        from_attributes = True
