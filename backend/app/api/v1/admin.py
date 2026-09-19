from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.user import User, UserRole, UserStatus
from app.api import deps

router = APIRouter()

@router.get("/pending-trainers")
def get_pending_trainers(
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_active_user)
):
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="Admin access required")

    trainers = (
        db.query(User)
        .filter(
            User.role == UserRole.TRAINER,
            User.status == UserStatus.PENDING
        )
        .all()
    )

    return [
        {
            "id": str(trainer.id),
            "name": trainer.name,
            "email": trainer.email,
            "role": trainer.role,
            "status": trainer.status,
            "created_at": trainer.created_at
        }
        for trainer in trainers
    ]

@router.put("/trainers/{trainer_id}/approve")
def approve_trainer(
    trainer_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_active_user)
):
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="Admin access required")

    trainer = (
        db.query(User)
        .filter(
            User.id == trainer_id,
            User.role == UserRole.TRAINER
        )
        .first()
    )

    if not trainer:
        raise HTTPException(status_code=404, detail="Trainer not found")

    if trainer.status == UserStatus.ACTIVE:
        raise HTTPException(status_code=400, detail="Trainer is already active")

    trainer.status = UserStatus.ACTIVE
    db.commit()
    db.refresh(trainer)

    return {
        "message": "Trainer approved successfully",
        "trainer_id": str(trainer.id),
        "status": trainer.status
    }