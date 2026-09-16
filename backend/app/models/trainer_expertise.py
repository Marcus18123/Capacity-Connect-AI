from sqlalchemy import Column, Integer, Float, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from app.models.base import BaseModel
from app.models.user_competency import VerificationStatus

class TrainerExpertise(BaseModel):
    __tablename__ = "trainer_expertise"

    trainer_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False)
    competency_id = Column(UUID(as_uuid=True), ForeignKey("competencies.id", ondelete="CASCADE"), index=True, nullable=False)
    proficiency_level = Column(Float, default=0.0)
    years_experience = Column(Integer, default=0)
    verification_status = Column(Enum(VerificationStatus), default=VerificationStatus.UNVERIFIED, nullable=False)

    trainer = relationship("User", back_populates="trainer_expertise")
    competency = relationship("Competency", back_populates="trainer_expertise")
