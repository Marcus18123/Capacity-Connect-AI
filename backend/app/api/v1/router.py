from fastapi import APIRouter
from app.api.v1 import auth, trainees, ai, admin, assessments, trainer

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(trainees.router, prefix="/trainees", tags=["Trainees"])
api_router.include_router(ai.router, prefix="/ai", tags=["AI - Skill Intelligence"])
api_router.include_router(admin.router, prefix="/admin", tags=["Administration"])
api_router.include_router(assessments.router, prefix="/assessments", tags=["Assessments"])
api_router.include_router(trainer.router, prefix="/trainer", tags=["Trainer"])