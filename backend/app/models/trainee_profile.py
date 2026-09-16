from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from app.models.base import BaseModel

class TraineeProfile(BaseModel):
    __tablename__ = "trainee_profiles"

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), unique=True, index=True, nullable=False)
    bio = Column(String, nullable=True)
    education = Column(String, nullable=True)
    current_role = Column(String, nullable=True)
    organization = Column(String, nullable=True)
    experience_years = Column(Integer, nullable=True)
    interests = Column(String, nullable=True)
    profile_photo_url = Column(String, nullable=True)

    user = relationship("User", back_populates="trainee_profile")
