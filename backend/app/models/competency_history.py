from sqlalchemy import Column, Float, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime, timezone
from app.models.base import BaseModel

class CompetencyHistory(BaseModel):
    __tablename__ = "competency_history"

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False)
    competency_id = Column(UUID(as_uuid=True), ForeignKey("competencies.id", ondelete="CASCADE"), index=True, nullable=False)
    old_level = Column(Float, nullable=True)
    new_level = Column(Float, nullable=False)
    source = Column(String, nullable=False) # ASSESSMENT, PROJECT, TRAINER, AI_ESTIMATE, COURSE
    confidence = Column(Float, default=0.0)
    changed_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    user = relationship("User")
    competency = relationship("Competency")
