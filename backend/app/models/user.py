from sqlalchemy import Column, String, Enum
from sqlalchemy.orm import relationship
import enum
from app.models.base import BaseModel

class UserRole(str, enum.Enum):
    TRAINEE = "TRAINEE"
    TRAINER = "TRAINER"
    ADMIN = "ADMIN"

class UserStatus(str, enum.Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    PENDING = "PENDING"
    SUSPENDED = "SUSPENDED"

class User(BaseModel):
    __tablename__ = "users"

    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(Enum(UserRole), nullable=False)
    status = Column(Enum(UserStatus), nullable=False, default=UserStatus.PENDING)

    trainee_profile = relationship("TraineeProfile", back_populates="user", uselist=False, cascade="all, delete-orphan")
    trainer_profile = relationship("TrainerProfile", back_populates="user", uselist=False, cascade="all, delete-orphan")
    user_competencies = relationship("UserCompetency", back_populates="user", foreign_keys="UserCompetency.user_id", cascade="all, delete-orphan")
    trainer_expertise = relationship("TrainerExpertise", back_populates="trainer", cascade="all, delete-orphan")
    enrollments = relationship("Enrollment", back_populates="trainee", cascade="all, delete-orphan")
    assessment_results = relationship("AssessmentResult", back_populates="trainee", cascade="all, delete-orphan")
    project_submissions = relationship("Submission", back_populates="trainee", cascade="all, delete-orphan")
    learning_paths = relationship("LearningPath", back_populates="trainee", cascade="all, delete-orphan")
    skill_gaps = relationship("SkillGap", back_populates="trainee", cascade="all, delete-orphan")
    notifications = relationship("Notification", back_populates="user", cascade="all, delete-orphan")
