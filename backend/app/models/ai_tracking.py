from sqlalchemy import Column, String, Integer, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from app.models.base import BaseModel

class AIRequest(BaseModel):
    __tablename__ = "ai_requests"

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False)
    feature = Column(String, index=True, nullable=False) # skill_extraction, gap_analysis, etc
    provider = Column(String, nullable=False) # mock, gemini, etc
    model_name = Column(String, nullable=False)
    request_status = Column(String, nullable=False) # SUCCESS, ERROR
    input_tokens = Column(Integer, default=0)
    output_tokens = Column(Integer, default=0)
    latency_ms = Column(Integer, default=0)
    error_message = Column(String, nullable=True)

    user = relationship("User")

class AIInsight(BaseModel):
    __tablename__ = "ai_insights"

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False)
    type = Column(String, index=True, nullable=False) # SKILL_GAP, LEARNING, etc
    title = Column(String, nullable=False)
    summary = Column(String, nullable=False)
    severity = Column(String, nullable=False) # LOW, MEDIUM, HIGH, CRITICAL
    source = Column(String, nullable=True)
    expires_at = Column(DateTime, nullable=True)

    user = relationship("User")
