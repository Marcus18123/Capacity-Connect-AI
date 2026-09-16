from sqlalchemy import Column, String, Boolean, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
import enum
from app.models.base import BaseModel

class CompetencyLevel(str, enum.Enum):
    BEGINNER = "BEGINNER"
    INTERMEDIATE = "INTERMEDIATE"
    ADVANCED = "ADVANCED"
    EXPERT = "EXPERT"

class Competency(BaseModel):
    __tablename__ = "competencies"

    name = Column(String, nullable=False, index=True)
    description = Column(String, nullable=True)
    category = Column(String, nullable=True, index=True)
    level = Column(Enum(CompetencyLevel), nullable=False)
    parent_id = Column(UUID(as_uuid=True), ForeignKey("competencies.id", ondelete="SET NULL"), nullable=True)
    is_active = Column(Boolean, default=True)

    parent = relationship("Competency", remote_side="Competency.id", backref="children")
    user_competencies = relationship("UserCompetency", back_populates="competency", cascade="all, delete-orphan")
    trainer_expertise = relationship("TrainerExpertise", back_populates="competency", cascade="all, delete-orphan")
    course_competencies = relationship("CourseCompetency", back_populates="competency", cascade="all, delete-orphan")
