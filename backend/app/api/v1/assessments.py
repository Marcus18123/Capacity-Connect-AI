from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

from app.core.database import get_db
from app.api import deps
from app.models.user import User, UserRole
from app.models.assessment import Assessment, AssessmentStatus
from app.models.question import Question
from app.models.assessment_result import AssessmentResult
from app.models.user_competency import UserCompetency, VerificationStatus, EvidenceSource

router = APIRouter()

class AnswerSubmission(BaseModel):
    question_id: str
    selected_option: str

class AssessmentSubmitPayload(BaseModel):
    answers: List[AnswerSubmission]

@router.get("/")
def get_assessments(
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_active_user)
):
    assessments = db.query(Assessment).all()
    user_results = {
        str(r.assessment_id): r 
        for r in db.query(AssessmentResult).filter(AssessmentResult.trainee_id == current_user.id).all()
    }
    
    output = []
    for a in assessments:
        result = user_results.get(str(a.id))
        output.append({
            "id": str(a.id),
            "title": a.title,
            "description": a.description,
            "duration_minutes": a.duration_minutes,
            "passing_score": a.passing_score,
            "question_count": len(a.questions),
            "status": "COMPLETED" if result and result.passed else ("TAKEN" if result else "AVAILABLE"),
            "last_score": result.score if result else None,
            "passed": result.passed if result else False
        })
    return output

@router.get("/{assessment_id}/questions")
def get_assessment_questions(
    assessment_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_active_user)
):
    assessment = db.query(Assessment).filter(Assessment.id == assessment_id).first()
    if not assessment:
        raise HTTPException(status_code=404, detail="Assessment not found")
        
    questions = db.query(Question).filter(Question.assessment_id == assessment.id).order_by(Question.order_index).all()
    
    return {
        "assessment_id": str(assessment.id),
        "title": assessment.title,
        "description": assessment.description,
        "duration_minutes": assessment.duration_minutes,
        "questions": [
            {
                "id": str(q.id),
                "question_text": q.question_text,
                "question_type": q.question_type.value if hasattr(q.question_type, "value") else str(q.question_type),
                "options": q.options,
                "marks": q.marks
            }
            for q in questions
        ]
    }

@router.post("/{assessment_id}/submit")
def submit_assessment(
    assessment_id: str,
    payload: AssessmentSubmitPayload,
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_active_user)
):
    assessment = db.query(Assessment).filter(Assessment.id == assessment_id).first()
    if not assessment:
        raise HTTPException(status_code=404, detail="Assessment not found")

    questions = db.query(Question).filter(Question.assessment_id == assessment.id).all()
    question_map = {str(q.id): q for q in questions}

    total_marks = sum(q.marks for q in questions) or 1
    obtained_marks = 0

    for ans in payload.answers:
        q = question_map.get(ans.question_id)
        if q and q.correct_answer and ans.selected_option.strip().lower() == q.correct_answer.strip().lower():
            obtained_marks += q.marks

    percentage = round((obtained_marks / total_marks) * 100, 2)
    passed = percentage >= assessment.passing_score

    # Save AssessmentResult
    result = AssessmentResult(
        assessment_id=assessment.id,
        trainee_id=current_user.id,
        score=obtained_marks,
        percentage=percentage,
        passed=passed,
        submitted_at=datetime.utcnow()
    )
    db.add(result)

    # If passed, upgrade user competency verification status
    if passed:
        for q in questions:
            if q.competency_id:
                uc = db.query(UserCompetency).filter(
                    UserCompetency.user_id == current_user.id,
                    UserCompetency.competency_id == q.competency_id
                ).first()
                if uc:
                    uc.verification_status = VerificationStatus.VERIFIED
                    uc.proficiency_level = min(5.0, (uc.proficiency_level or 2.0) + 1.0)
                    uc.evidence_source = EvidenceSource.ASSESSMENT
                    uc.confidence = 0.95

    db.commit()

    return {
        "assessment_id": str(assessment.id),
        "score": obtained_marks,
        "total_marks": total_marks,
        "percentage": percentage,
        "passed": passed,
        "message": "Congratulations! You passed the assessment." if passed else "Keep learning and try again."
    }
