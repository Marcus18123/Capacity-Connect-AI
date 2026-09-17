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
    AI_ESTIMATED = "AI_ESTIMATED"
    EXPIRED = "EXPIRED"

class EvidenceSource(str, enum.Enum):
    SELF_REPORTED = "SELF_REPORTED"
    AI_EXTRACTED = "AI_EXTRACTED"
    COURSE_COMPLETION = "COURSE_COMPLETION"
    ASSESSMENT = "ASSESSMENT"
    PROJECT = "PROJECT"
    TRAINER_VERIFIED = "TRAINER_VERIFIED"

class UserCompetency(BaseModel):
    __tablename__ = "user_competencies"

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False)
    competency_id = Column(UUID(as_uuid=True), ForeignKey("competencies.id", ondelete="CASCADE"), index=True, nullable=False)
    proficiency_level = Column(Float, default=0.0)
    verification_status = Column(Enum(VerificationStatus), default=VerificationStatus.UNVERIFIED, nullable=False)
    evidence_source = Column(Enum(EvidenceSource), default=EvidenceSource.SELF_REPORTED, nullable=False)
    confidence = Column(Float, default=0.0)
    evidence_url = Column(String, nullable=True)
    last_assessed_at = Column(DateTime, nullable=True)
    verified_by = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    verified_at = Column(DateTime, nullable=True)

    user = relationship("User", back_populates="user_competencies", foreign_keys=[user_id])
    verifier = relationship("User", foreign_keys=[verified_by])
    competency = relationship("Competency", back_populates="user_competencies")
