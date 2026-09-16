from sqlalchemy import Column, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from app.models.base import BaseModel

class Project(BaseModel):
    __tablename__ = "projects"

    course_id = Column(UUID(as_uuid=True), ForeignKey("courses.id", ondelete="SET NULL"), nullable=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    instructions = Column(String, nullable=True)
    rubric = Column(String, nullable=True)
    deadline = Column(DateTime, nullable=True)
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True)

    course = relationship("Course", back_populates="projects")
    submissions = relationship("Submission", back_populates="project", cascade="all, delete-orphan")
