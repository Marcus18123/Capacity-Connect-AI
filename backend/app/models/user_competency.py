from sqlalchemy import Column, Integer, String, Float, ForeignKey, Enum, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
import enum
from app.models.base import BaseModel

class VerificationStatus(str, enum.Enum):
    UNVERIFIED = "UNVERIFIED"
    LEARNING = "LEARNING"
    ASSESSED = "ASSESSED"
    VERIFIED = "VERIFIED"
    EXPIRED = "EXPIRED"

class UserCompetency(BaseModel):
    __tablename__ = "user_competencies"

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False)
    competency_id = Column(UUID(as_uuid=True), ForeignKey("competencies.id", ondelete="CASCADE"), index=True, nullable=False)
    proficiency_level = Column(Float, default=0.0)
    verification_status = Column(Enum(VerificationStatus), default=VerificationStatus.UNVERIFIED, nullable=False)
    confidence = Column(Float, default=0.0)
    evidence_url = Column(String, nullable=True)
    last_assessed_at = Column(DateTime, nullable=True)

    user = relationship("User", back_populates="user_competencies")
    competency = relationship("Competency", back_populates="user_competencies")
