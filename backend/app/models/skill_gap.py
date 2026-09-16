from sqlalchemy import Column, String, Float, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from app.models.base import BaseModel
from app.models.learning_path_item import Priority
from app.models.competency import CompetencyLevel

class SkillGapStatus(str, enum.Enum):
    IDENTIFIED = "IDENTIFIED"
    IN_PROGRESS = "IN_PROGRESS"
    RESOLVED = "RESOLVED"

class SkillGap(BaseModel):
    __tablename__ = "skill_gaps"

    trainee_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False)
    competency_id = Column(UUID(as_uuid=True), ForeignKey("competencies.id", ondelete="CASCADE"), index=True, nullable=False)
    current_level = Column(Enum(CompetencyLevel), nullable=False)
    target_level = Column(Enum(CompetencyLevel), nullable=False)
    gap_percentage = Column(Float, default=0.0)
    priority = Column(Enum(Priority), default=Priority.MEDIUM, nullable=False)
    reason = Column(String, nullable=True)
    status = Column(Enum(SkillGapStatus), default=SkillGapStatus.IDENTIFIED, nullable=False)

    trainee = relationship("User", back_populates="skill_gaps")
    competency = relationship("Competency")
