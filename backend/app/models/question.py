from sqlalchemy import Column, String, Integer, ForeignKey, Enum
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
import enum
from app.models.base import BaseModel

class QuestionType(str, enum.Enum):
    MCQ = "MCQ"
    TRUE_FALSE = "TRUE_FALSE"
    SHORT_ANSWER = "SHORT_ANSWER"
    DESCRIPTIVE = "DESCRIPTIVE"

class Question(BaseModel):
    __tablename__ = "questions"

    assessment_id = Column(UUID(as_uuid=True), ForeignKey("assessments.id", ondelete="CASCADE"), index=True, nullable=False)
    competency_id = Column(UUID(as_uuid=True), ForeignKey("competencies.id", ondelete="SET NULL"), nullable=True)
    question_text = Column(String, nullable=False)
    question_type = Column(Enum(QuestionType), nullable=False)
    difficulty = Column(String, nullable=True)
    options = Column(JSONB, nullable=True)
    correct_answer = Column(String, nullable=True)
    explanation = Column(String, nullable=True)
    marks = Column(Integer, default=1)
    order_index = Column(Integer, default=0)

    assessment = relationship("Assessment", back_populates="questions")
