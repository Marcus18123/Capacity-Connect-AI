from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from uuid import UUID
from app.models.user import UserRole, UserStatus
from app.models.trainer_profile import ApprovalStatus

class TraineeProfileBase(BaseModel):
    bio: Optional[str] = None
    education: Optional[str] = None
    current_role: Optional[str] = None
    organization: Optional[str] = None
    experience_years: Optional[int] = None
    interests: Optional[str] = None
    profile_photo_url: Optional[str] = None

class TrainerProfileBase(BaseModel):
    professional_title: Optional[str] = None
    bio: Optional[str] = None
    organization: Optional[str] = None
    experience_years: Optional[int] = None
    availability: Optional[str] = None
    languages: Optional[str] = None
    profile_photo_url: Optional[str] = None
    approval_status: Optional[ApprovalStatus] = None

class UserBase(BaseModel):
    name: str
    email: EmailStr
    role: UserRole

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: UUID
    status: UserStatus
    created_at: datetime
    
    trainee_profile: Optional[TraineeProfileBase] = None
    trainer_profile: Optional[TrainerProfileBase] = None

    class Config:
        from_attributes = True
