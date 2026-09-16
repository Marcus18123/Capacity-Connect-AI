from sqlalchemy import Column, String, Integer, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
import enum
from app.models.base import BaseModel

class ApprovalStatus(str, enum.Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"

class TrainerProfile(BaseModel):
    __tablename__ = "trainer_profiles"

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), unique=True, index=True, nullable=False)
    professional_title = Column(String, nullable=True)
    bio = Column(String, nullable=True)
    organization = Column(String, nullable=True)
    experience_years = Column(Integer, nullable=True)
    availability = Column(String, nullable=True)
    languages = Column(String, nullable=True)
    profile_photo_url = Column(String, nullable=True)
    approval_status = Column(Enum(ApprovalStatus), default=ApprovalStatus.PENDING, nullable=False)

    user = relationship("User", back_populates="trainer_profile")
