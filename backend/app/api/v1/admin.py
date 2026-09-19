from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.user import User, UserRole, UserStatus
from app.api import deps

router = APIRouter()

@router.get("/metrics")
def get_admin_metrics(
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_active_user)
):
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="Admin access required")

    total_trainees = db.query(User).filter(User.role == UserRole.TRAINEE).count()
    total_trainers = db.query(User).filter(User.role == UserRole.TRAINER, User.status == UserStatus.ACTIVE).count()
    pending_trainers = db.query(User).filter(User.role == UserRole.TRAINER, User.status == UserStatus.PENDING).count()

    return {
        "metrics": {
            "total_trainees": total_trainees,
            "total_trainers": total_trainers,
            "pending_trainers": pending_trainers
        }
    }

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
            "role": trainer.role.value if hasattr(trainer.role, "value") else str(trainer.role),
            "status": trainer.status.value if hasattr(trainer.status, "value") else str(trainer.status),
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

    trainer.status = UserStatus.ACTIVE
    if trainer.trainer_profile:
        from app.models.trainer_profile import ApprovalStatus
        trainer.trainer_profile.approval_status = ApprovalStatus.APPROVED

    db.commit()
    return {"message": "Trainer approved successfully", "trainer_id": str(trainer.id), "status": "ACTIVE"}

@router.put("/trainers/{trainer_id}/reject")
def reject_trainer(
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

    trainer.status = UserStatus.REJECTED
    if trainer.trainer_profile:
        from app.models.trainer_profile import ApprovalStatus
        trainer.trainer_profile.approval_status = ApprovalStatus.REJECTED

    db.commit()
    return {"message": "Trainer rejected", "trainer_id": str(trainer.id), "status": "REJECTED"}