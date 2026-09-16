from sqlalchemy import Column, String, Boolean, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
import enum
from app.models.base import BaseModel

class NotificationType(str, enum.Enum):
    COURSE = "COURSE"
    ASSESSMENT = "ASSESSMENT"
    COMPETENCY = "COMPETENCY"
    TRAINER = "TRAINER"
    SYSTEM = "SYSTEM"
    AI_INSIGHT = "AI_INSIGHT"

class Notification(BaseModel):
    __tablename__ = "notifications"

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False)
    title = Column(String, nullable=False)
    message = Column(String, nullable=False)
    type = Column(Enum(NotificationType), default=NotificationType.SYSTEM, nullable=False)
    is_read = Column(Boolean, default=False)

    user = relationship("User", back_populates="notifications")
