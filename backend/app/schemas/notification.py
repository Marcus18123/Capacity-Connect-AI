from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from datetime import datetime
from app.models.notification import NotificationType

class NotificationBase(BaseModel):
    title: str
    message: str
    type: NotificationType
    is_read: bool = False

class NotificationResponse(NotificationBase):
    id: UUID
    user_id: UUID
    created_at: datetime
    
    class Config:
        from_attributes = True
