from sqlalchemy import Column, String, Float, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
import enum
from app.models.base import BaseModel

class LearningPathStatus(str, enum.Enum):
    ACTIVE = "ACTIVE"
    COMPLETED = "COMPLETED"
    ARCHIVED = "ARCHIVED"

class GenerationMethod(str, enum.Enum):
    MANUAL = "MANUAL"
    SYSTEM = "SYSTEM"
    AI = "AI"

class LearningPath(BaseModel):
    __tablename__ = "learning_paths"

    trainee_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False)
    target_role = Column(String, nullable=False)
    current_alignment = Column(Float, default=0.0)
    status = Column(Enum(LearningPathStatus), default=LearningPathStatus.ACTIVE, nullable=False)
    generated_by = Column(Enum(GenerationMethod), default=GenerationMethod.SYSTEM, nullable=False)

    trainee = relationship("User", back_populates="learning_paths")
    items = relationship("LearningPathItem", back_populates="learning_path", cascade="all, delete-orphan", order_by="LearningPathItem.sequence")
