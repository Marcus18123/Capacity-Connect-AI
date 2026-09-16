from sqlalchemy import Column, Float, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from app.models.base import BaseModel
from app.models.competency import CompetencyLevel

class CourseCompetency(BaseModel):
    __tablename__ = "course_competencies"

    course_id = Column(UUID(as_uuid=True), ForeignKey("courses.id", ondelete="CASCADE"), index=True, nullable=False)
    competency_id = Column(UUID(as_uuid=True), ForeignKey("competencies.id", ondelete="CASCADE"), index=True, nullable=False)
    target_level = Column(Enum(CompetencyLevel), nullable=False)
    importance = Column(Float, default=1.0)

    course = relationship("Course", back_populates="course_competencies")
    competency = relationship("Competency", back_populates="course_competencies")
