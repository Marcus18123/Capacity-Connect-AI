from fastapi import APIRouter
from app.api.v1 import auth, trainees, ai

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(trainees.router, prefix="/trainees", tags=["Trainees"])
api_router.include_router(ai.router, prefix="/ai", tags=["AI - Skill Intelligence"])
# Other routers (Trainers, Competencies, Courses, Admin) will be mounted here
