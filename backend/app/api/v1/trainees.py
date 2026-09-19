from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.api import deps
from app.models.user import User, UserRole, UserStatus
from app.models.enrollment import Enrollment, EnrollmentStatus
from app.models.user_competency import UserCompetency, VerificationStatus
from app.models.role import Role, RoleCompetency
from app.models.learning_path import LearningPath, LearningPathStatus, GenerationMethod
from app.models.learning_path_item import LearningPathItem, PathItemStatus, Priority
from app.models.trainer_profile import TrainerProfile, ApprovalStatus
from app.models.trainer_expertise import TrainerExpertise

router = APIRouter()

@router.get("/me/dashboard")
def get_trainee_dashboard(
    current_user: User = Depends(deps.require_role([UserRole.TRAINEE])),
    db: Session = Depends(get_db)
):
    user_competencies = (
        db.query(UserCompetency)
        .filter(UserCompetency.user_id == current_user.id)
        .all()
    )

    competency_index = 0.0
    if user_competencies:
        competency_index = round(
            sum(min(max(uc.proficiency_level or 0, 0), 5) for uc in user_competencies)
            / (len(user_competencies) * 5) * 100,
            2
        )

    verified_competencies = sum(
        1
        for uc in user_competencies
        if uc.verification_status == VerificationStatus.VERIFIED
    )

    role = (
        db.query(Role)
        .filter(Role.name == "Data Analyst")
        .first()
    )

    skill_gap_count = 0

    if role:
        role_competencies = (
            db.query(RoleCompetency)
            .filter(RoleCompetency.role_id == role.id)
            .all()
        )

        user_levels = {
            uc.competency_id: uc.proficiency_level or 0
            for uc in user_competencies
        }

        skill_gap_count = sum(
            1
            for rc in role_competencies
            if user_levels.get(rc.competency_id, 0) < (rc.required_level or 0)
        )

    active_courses = (
        db.query(Enrollment)
        .filter(
            Enrollment.trainee_id == current_user.id,
            Enrollment.status.in_([
                EnrollmentStatus.ENROLLED,
                EnrollmentStatus.IN_PROGRESS
            ])
        )
        .count()
    )

    return {
        "user": {
            "id": str(current_user.id),
            "name": current_user.name,
            "role": current_user.role
        },
        "kpis": {
            "competency_index": competency_index,
            "active_courses": active_courses,
            "skill_gap_count": skill_gap_count,
            "verified_competencies": verified_competencies
        },
        "recent_activity": []
    }

@router.get("/me/competencies")
def get_trainee_competencies(
    current_user: User = Depends(deps.require_role([UserRole.TRAINEE])),
    db: Session = Depends(get_db)
):
    competencies = (
        db.query(UserCompetency)
        .filter(UserCompetency.user_id == current_user.id)
        .all()
    )

    return [
        {
            "id": str(item.id),
            "competency_id": str(item.competency_id),
            "name": item.competency.name,
            "description": item.competency.description,
            "category": item.competency.category,
            "level": item.competency.level.value,
            "proficiency_level": item.proficiency_level,
            "verification_status": item.verification_status.value,
            "evidence_source": item.evidence_source.value,
            "confidence": item.confidence,
            "evidence_url": item.evidence_url,
            "last_assessed_at": item.last_assessed_at
        }
        for item in competencies
    ]

@router.get("/me/skill-gaps")
def get_trainee_skill_gaps(
    current_user: User = Depends(deps.require_role([UserRole.TRAINEE])),
    db: Session = Depends(get_db)
):
    target_role = (
        db.query(Role)
        .filter(
            Role.name == "Data Analyst",
            Role.is_active == True
        )
        .first()
    )

    if not target_role:
        raise HTTPException(
            status_code=404,
            detail="Target role not found"
        )

    required_competencies = (
        db.query(RoleCompetency)
        .filter(RoleCompetency.role_id == target_role.id)
        .all()
    )

    user_competencies = {
        item.competency_id: item
        for item in db.query(UserCompetency)
        .filter(UserCompetency.user_id == current_user.id)
        .all()
    }

    skill_gaps = []
    weighted_alignment = 0.0
    total_weight = 0.0

    for requirement in required_competencies:
        current = user_competencies.get(requirement.competency_id)

        current_level = current.proficiency_level if current else 0.0
        required_level = requirement.required_level
        gap = max(required_level - current_level, 0.0)

        importance = requirement.importance or 1.0
        total_weight += importance

        achieved_ratio = min(current_level / required_level, 1.0) if required_level > 0 else 1.0
        weighted_alignment += achieved_ratio * importance

        skill_gaps.append({
            "competency_id": str(requirement.competency_id),
            "competency": requirement.competency.name,
            "current_level": current_level,
            "required_level": required_level,
            "gap": gap,
            "importance": importance,
            "status": "GAP" if gap > 0 else "MET"
        })

    overall_alignment = (
        round((weighted_alignment / total_weight) * 100, 2)
        if total_weight > 0 else 0
    )

    return {
        "target_role": target_role.name,
        "overall_alignment": overall_alignment,
        "skill_gaps": skill_gaps
    }

@router.get("/me/learning-path")
def get_trainee_learning_path(
    current_user: User = Depends(deps.require_role([UserRole.TRAINEE])),
    db: Session = Depends(get_db)
):
    target_role = (
        db.query(Role)
        .filter(
            Role.name == "Data Analyst",
            Role.is_active == True
        )
        .first()
    )

    if not target_role:
        raise HTTPException(
            status_code=404,
            detail="Target role not found"
        )

    required_competencies = (
        db.query(RoleCompetency)
        .filter(RoleCompetency.role_id == target_role.id)
        .all()
    )

    user_competencies = {
        item.competency_id: item
        for item in db.query(UserCompetency)
        .filter(UserCompetency.user_id == current_user.id)
        .all()
    }

    gaps = []

    for requirement in required_competencies:
        current = user_competencies.get(requirement.competency_id)
        current_level = current.proficiency_level if current else 0.0
        required_level = requirement.required_level
        gap = max(required_level - current_level, 0.0)

        if gap > 0:
            gaps.append({
                "competency_id": requirement.competency_id,
                "competency": requirement.competency.name,
                "current_level": current_level,
                "required_level": required_level,
                "gap": gap,
                "importance": requirement.importance or 1.0
            })

    total_weight = sum(
        requirement.importance or 1.0
        for requirement in required_competencies
    )

    weighted_alignment = 0.0

    for requirement in required_competencies:
        current = user_competencies.get(requirement.competency_id)
        current_level = current.proficiency_level if current else 0.0
        required_level = requirement.required_level
        importance = requirement.importance or 1.0

        ratio = (
            min(current_level / required_level, 1.0)
            if required_level > 0 else 1.0
        )

        weighted_alignment += ratio * importance

    current_alignment = (
        round((weighted_alignment / total_weight) * 100, 2)
        if total_weight > 0 else 0
    )

    learning_path = (
        db.query(LearningPath)
        .filter(
            LearningPath.trainee_id == current_user.id,
            LearningPath.status == LearningPathStatus.ACTIVE
        )
        .first()
    )

    if not learning_path:
        learning_path = LearningPath(
            trainee_id=current_user.id,
            target_role=target_role.name,
            current_alignment=current_alignment,
            status=LearningPathStatus.ACTIVE,
            generated_by=GenerationMethod.SYSTEM
        )

        db.add(learning_path)
        db.flush()

        for index, gap in enumerate(
            sorted(
                gaps,
                key=lambda item: (
                    item["importance"] * item["gap"]
                ),
                reverse=True
            ),
            start=1
        ):
            if gap["gap"] >= 2:
                priority = Priority.HIGH
            elif gap["gap"] >= 1:
                priority = Priority.MEDIUM
            else:
                priority = Priority.LOW

            db.add(
                LearningPathItem(
                    learning_path_id=learning_path.id,
                    competency_id=gap["competency_id"],
                    sequence=index,
                    priority=priority,
                    status=(
                        PathItemStatus.AVAILABLE
                        if index == 1
                        else PathItemStatus.LOCKED
                    ),
                    progress_percentage=0.0
                )
            )

        db.commit()
        db.refresh(learning_path)

    return {
        "id": str(learning_path.id),
        "target_role": learning_path.target_role,
        "current_alignment": learning_path.current_alignment,
        "status": learning_path.status.value,
        "generated_by": learning_path.generated_by.value,
        "items": [
            {
                "id": str(item.id),
                "sequence": item.sequence,
                "competency": (
                    item.competency.name
                    if item.competency else None
                ),
                "competency_id": (
                    str(item.competency_id)
                    if item.competency_id else None
                ),
                "priority": item.priority.value,
                "status": item.status.value,
                "progress_percentage": item.progress_percentage
            }
            for item in learning_path.items
        ]
    }

@router.put("/me/learning-path/items/{item_id}/status")
def update_learning_path_item_status(
    item_id: str,
    status_update: dict,
    current_user: User = Depends(deps.require_role([UserRole.TRAINEE])),
    db: Session = Depends(get_db)
):
    item = (
        db.query(LearningPathItem)
        .join(LearningPath, LearningPathItem.learning_path_id == LearningPath.id)
        .filter(
            LearningPathItem.id == item_id,
            LearningPath.trainee_id == current_user.id
        )
        .first()
    )

    if not item:
        raise HTTPException(status_code=404, detail="Learning path item not found")

    new_status = status_update.get("status")
    if new_status and new_status in PathItemStatus.__members__:
        item.status = PathItemStatus[new_status]
        if new_status == "COMPLETED":
            item.progress_percentage = 100.0
            # Unlock the next item if available
            next_item = (
                db.query(LearningPathItem)
                .filter(
                    LearningPathItem.learning_path_id == item.learning_path_id,
                    LearningPathItem.sequence == item.sequence + 1
                )
                .first()
            )
            if next_item and next_item.status == PathItemStatus.LOCKED:
                next_item.status = PathItemStatus.AVAILABLE

        elif new_status == "IN_PROGRESS":
            item.progress_percentage = status_update.get("progress_percentage", 50.0)

    db.commit()
    db.refresh(item)

    return {
        "id": str(item.id),
        "status": item.status.value,
        "progress_percentage": item.progress_percentage
    }


@router.get("/me/recommended-trainers")
def get_recommended_trainers(
    current_user: User = Depends(deps.require_role([UserRole.TRAINEE])),
    db: Session = Depends(get_db)
):
    user_competencies = {
        item.competency_id: item
        for item in db.query(UserCompetency)
        .filter(UserCompetency.user_id == current_user.id)
        .all()
    }

    skill_gaps = []

    target_role = (
        db.query(Role)
        .filter(
            Role.name == "Data Analyst",
            Role.is_active == True
        )
        .first()
    )

    if target_role:
        requirements = (
            db.query(RoleCompetency)
            .filter(RoleCompetency.role_id == target_role.id)
            .all()
        )

        for requirement in requirements:
            current = user_competencies.get(requirement.competency_id)
            current_level = current.proficiency_level if current else 0.0
            gap = max(
                requirement.required_level - current_level,
                0.0
            )

            if gap > 0:
                skill_gaps.append({
                    "competency_id": requirement.competency_id,
                    "competency": requirement.competency.name,
                    "gap": gap,
                    "importance": requirement.importance or 1.0
                })

    trainers = (
        db.query(User)
        .join(
            TrainerProfile,
            TrainerProfile.user_id == User.id
        )
        .filter(
            User.role == UserRole.TRAINER,
            User.status == UserStatus.ACTIVE,
            TrainerProfile.approval_status == ApprovalStatus.APPROVED
        )
        .all()
    )

    recommendations = []

    for trainer in trainers:
        expertise = (
            db.query(TrainerExpertise)
            .filter(
                TrainerExpertise.trainer_id == trainer.id
            )
            .all()
        )

        if not expertise:
            continue

        expertise_by_competency = {
            item.competency_id: item
            for item in expertise
        }

        weighted_match = 0.0
        total_weight = 0.0
        matched_competencies = []

        for gap in skill_gaps:
            trainer_expertise = expertise_by_competency.get(
                gap["competency_id"]
            )

            if not trainer_expertise:
                continue

            trainer_level = trainer_expertise.proficiency_level
            match_ratio = min(trainer_level / 5.0, 1.0)

            weight = gap["importance"] * gap["gap"]
            weighted_match += match_ratio * weight
            total_weight += weight

            matched_competencies.append(
                gap["competency"]
            )

        match_score = (
            round((weighted_match / total_weight) * 100, 2)
            if total_weight > 0 else 0
        )

        recommendations.append({
            "id": str(trainer.id),
            "name": trainer.name,
            "experience": (
                f"{trainer.trainer_profile.experience_years or 0} years"
            ),
            "availability": (
                trainer.trainer_profile.availability or "Not specified"
            ),
            "matchScore": match_score,
            "expertise": ", ".join(
                item.competency.name
                for item in expertise
            ),
            "matchedCompetencies": matched_competencies,
            "reason": (
                f"Strong expertise in "
                f"{', '.join(matched_competencies)}"
                f", directly aligned with your current skill gaps."
                if matched_competencies
                else "Trainer expertise does not directly match your current skill gaps."
            )
        })

    recommendations.sort(
        key=lambda trainer: trainer["matchScore"],
        reverse=True
    )

    return recommendations
