from sqlalchemy import Column, Integer, Float, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
from app.models.base import BaseModel

class AssessmentResult(BaseModel):
    __tablename__ = "assessment_results"

    assessment_id = Column(UUID(as_uuid=True), ForeignKey("assessments.id", ondelete="CASCADE"), index=True, nullable=False)
    trainee_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False)
    score = Column(Integer, default=0)
    percentage = Column(Float, default=0.0)
    passed = Column(Boolean, default=False)
    attempt_number = Column(Integer, default=1)
    submitted_at = Column(DateTime, default=datetime.utcnow)

    assessment = relationship("Assessment", back_populates="results")
    trainee = relationship("User", back_populates="assessment_results")
