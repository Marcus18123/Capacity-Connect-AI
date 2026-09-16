from sqlalchemy import Column, String, Integer, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
import enum
from app.models.base import BaseModel

class CourseStatus(str, enum.Enum):
    DRAFT = "DRAFT"
    PENDING_APPROVAL = "PENDING_APPROVAL"
    PUBLISHED = "PUBLISHED"
    ARCHIVED = "ARCHIVED"

class CourseDifficulty(str, enum.Enum):
    BEGINNER = "BEGINNER"
    INTERMEDIATE = "INTERMEDIATE"
    ADVANCED = "ADVANCED"
    EXPERT = "EXPERT"

class Course(BaseModel):
    __tablename__ = "courses"

    trainer_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True)
    title = Column(String, nullable=False, index=True)
    description = Column(String, nullable=True)
    category = Column(String, nullable=True, index=True)
    difficulty = Column(Enum(CourseDifficulty), nullable=False)
    duration_minutes = Column(Integer, default=0)
    status = Column(Enum(CourseStatus), default=CourseStatus.DRAFT, nullable=False)
    thumbnail_url = Column(String, nullable=True)

    course_competencies = relationship("CourseCompetency", back_populates="course", cascade="all, delete-orphan")
    enrollments = relationship("Enrollment", back_populates="course", cascade="all, delete-orphan")
    assessments = relationship("Assessment", back_populates="course", cascade="all, delete-orphan")
    projects = relationship("Project", back_populates="course", cascade="all, delete-orphan")
