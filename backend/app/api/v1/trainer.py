from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional

from app.core.database import get_db
from app.api import deps
from app.models.user import User, UserRole, UserStatus
from app.models.trainer_profile import TrainerProfile
from app.models.trainer_expertise import TrainerExpertise
from app.models.user_competency import UserCompetency
from app.models.competency import Competency

router = APIRouter()

class ExpertiseCreate(BaseModel):
    competency_id: str
    proficiency_level: float
    years_experience: int

@router.get("/dashboard")
def get_trainer_dashboard(
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.require_role([UserRole.TRAINER]))
):
    profile = db.query(TrainerProfile).filter(TrainerProfile.user_id == current_user.id).first()
    expertise_list = db.query(TrainerExpertise).filter(TrainerExpertise.trainer_id == current_user.id).all()
    
    # Get all active trainees in system
    trainees = db.query(User).filter(User.role == UserRole.TRAINEE, User.status == UserStatus.ACTIVE).all()
    
    trainee_summaries = []
    for t in trainees:
        comps = db.query(UserCompetency).filter(UserCompetency.user_id == t.id).all()
        avg_level = round(sum(c.proficiency_level or 0 for c in comps) / len(comps), 2) if comps else 0.0
        trainee_summaries.append({
            "id": str(t.id),
            "name": t.name,
            "email": t.email,
            "competencies_count": len(comps),
            "average_proficiency": avg_level
        })
        
    return {
        "trainer": {
            "id": str(current_user.id),
            "name": current_user.name,
            "title": profile.professional_title if profile else "Trainer",
            "approval_status": profile.approval_status.value if profile else "APPROVED"
        },
        "expertise": [
            {
                "id": str(e.id),
                "competency": e.competency.name if e.competency else "Unknown",
                "proficiency_level": e.proficiency_level,
                "years_experience": e.years_experience
            }
            for e in expertise_list
        ],
        "assigned_trainees": trainee_summaries
    }

@router.post("/expertise")
def add_trainer_expertise(
    payload: ExpertiseCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.require_role([UserRole.TRAINER]))
):
    comp = db.query(Competency).filter(Competency.id == payload.competency_id).first()
    if not comp:
        raise HTTPException(status_code=404, detail="Competency not found")

    existing = db.query(TrainerExpertise).filter(
        TrainerExpertise.trainer_id == current_user.id,
        TrainerExpertise.competency_id == payload.competency_id
    ).first()

    if existing:
        existing.proficiency_level = payload.proficiency_level
        existing.years_experience = payload.years_experience
    else:
        existing = TrainerExpertise(
            trainer_id=current_user.id,
            competency_id=payload.competency_id,
            proficiency_level=payload.proficiency_level,
            years_experience=payload.years_experience
        )
        db.add(existing)

    db.commit()
    db.refresh(existing)
    return {"message": "Expertise updated successfully", "id": str(existing.id)}
