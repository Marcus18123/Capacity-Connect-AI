from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from uuid import UUID
from datetime import datetime
from app.models.assessment import AssessmentStatus
from app.models.question import QuestionType

class QuestionBase(BaseModel):
    question_text: str
    question_type: QuestionType
    difficulty: Optional[str] = None
    options: Optional[Dict[str, Any]] = None
    correct_answer: Optional[str] = None
    explanation: Optional[str] = None
    marks: int = 1
    order_index: int = 0

class QuestionResponse(QuestionBase):
    id: UUID
    assessment_id: UUID
    competency_id: Optional[UUID] = None
    
    class Config:
        from_attributes = True

class AssessmentBase(BaseModel):
    title: str
    description: Optional[str] = None
    duration_minutes: int
    passing_score: int
    deadline: Optional[datetime] = None

class AssessmentResponse(AssessmentBase):
    id: UUID
    course_id: Optional[UUID] = None
    status: AssessmentStatus
    created_by: Optional[UUID] = None
    created_at: datetime
    
    questions: Optional[List[QuestionResponse]] = None

    class Config:
        from_attributes = True

class AssessmentSubmission(BaseModel):
    answers: Dict[str, str] # e.g. {"question_id": "answer"}

class AssessmentResultResponse(BaseModel):
    id: UUID
    assessment_id: UUID
    trainee_id: UUID
    score: int
    percentage: float
    passed: bool
    attempt_number: int
    submitted_at: datetime

    class Config:
        from_attributes = True
