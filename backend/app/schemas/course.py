from pydantic import BaseModel
from typing import Optional, List
from uuid import UUID
from datetime import datetime
from app.models.course import CourseStatus, CourseDifficulty
from app.schemas.competency import CompetencyResponse

class CourseBase(BaseModel):
    title: str
    description: Optional[str] = None
    category: Optional[str] = None
    difficulty: CourseDifficulty
    duration_minutes: int
    thumbnail_url: Optional[str] = None

class CourseCreate(CourseBase):
    pass

class CourseResponse(CourseBase):
    id: UUID
    trainer_id: Optional[UUID] = None
    status: CourseStatus
    created_at: datetime
    
    class Config:
        from_attributes = True

class EnrollmentBase(BaseModel):
    course_id: UUID

class EnrollmentResponse(EnrollmentBase):
    id: UUID
    trainee_id: UUID
    progress_percentage: float
    status: str
    enrolled_at: datetime
    completed_at: Optional[datetime] = None
    
    course: Optional[CourseResponse] = None

    class Config:
        from_attributes = True
