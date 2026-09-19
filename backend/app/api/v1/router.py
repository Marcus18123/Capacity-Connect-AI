from fastapi import APIRouter
from app.api.v1 import auth, trainees, ai, admin

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(trainees.router, prefix="/trainees", tags=["Trainees"])
api_router.include_router(ai.router, prefix="/ai", tags=["AI - Skill Intelligence"])
api_router.include_router(admin.router, prefix="/admin", tags=["Administration"])