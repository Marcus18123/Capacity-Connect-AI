from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Dict, Any
from app.core.database import get_db
from app.api import deps
from app.models.user import User, UserRole

router = APIRouter()

@router.get("/me/dashboard")
def get_trainee_dashboard(
    current_user: User = Depends(deps.require_role([UserRole.TRAINEE])),
    db: Session = Depends(get_db)
):
    # This endpoint aggregates dashboard data.
    # In a real scenario, this would query enrollments, competencies, skill gaps, etc.
    # For Phase 2 frontend integration, we return a structured payload.
    return {
        "user": {
            "name": current_user.name,
            "role": current_user.role,
            "id": str(current_user.id)
        },
        "kpis": {
            "competency_index": 72,
            "active_courses": 2,
            "skill_gap_count": 3,
            "verified_competencies": 5
        },
        "recent_activity": []
    }

@router.get("/me/competencies")
def get_trainee_competencies(
    current_user: User = Depends(deps.require_role([UserRole.TRAINEE])),
    db: Session = Depends(get_db)
):
    # Return user competencies
    return []

@router.get("/me/skill-gaps")
def get_trainee_skill_gaps(
    current_user: User = Depends(deps.require_role([UserRole.TRAINEE])),
    db: Session = Depends(get_db)
):
    return {
        "target_role": "Data Scientist",
        "overall_alignment": 65,
        "skill_gaps": []
    }

@router.get("/me/learning-path")
def get_trainee_learning_path(
    current_user: User = Depends(deps.require_role([UserRole.TRAINEE])),
    db: Session = Depends(get_db)
):
    return {
        "target_role": "Data Scientist",
        "current_alignment": 65,
        "items": []
    }

@router.get("/me/recommended-trainers")
def get_recommended_trainers(
    current_user: User = Depends(deps.require_role([UserRole.TRAINEE])),
    db: Session = Depends(get_db)
):
    # Rule-based trainer matching
    return []
