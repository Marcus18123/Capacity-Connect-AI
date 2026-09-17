from sqlalchemy import Column, String, Boolean, ForeignKey, Integer, Float
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from app.models.base import BaseModel

class Role(BaseModel):
    __tablename__ = "roles"

    name = Column(String, index=True, nullable=False)
    description = Column(String, nullable=True)
    industry = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)

    role_competencies = relationship("RoleCompetency", back_populates="role", cascade="all, delete-orphan")

class RoleCompetency(BaseModel):
    __tablename__ = "role_competencies"

    role_id = Column(UUID(as_uuid=True), ForeignKey("roles.id", ondelete="CASCADE"), index=True, nullable=False)
    competency_id = Column(UUID(as_uuid=True), ForeignKey("competencies.id", ondelete="CASCADE"), index=True, nullable=False)
    required_level = Column(Float, default=1.0) # E.g. 1.0 (Beginner) to 4.0 (Expert)
    minimum_level = Column(Float, default=1.0)
    importance = Column(Float, default=1.0) # Multiplier for priority calculation

    role = relationship("Role", back_populates="role_competencies")
    competency = relationship("Competency")
