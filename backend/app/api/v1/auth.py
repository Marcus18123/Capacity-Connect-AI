from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import create_access_token, create_refresh_token
from app.schemas.auth import Token, TokenPayload, TokenRefresh
from app.schemas.user import UserCreate, UserResponse
from app.services import auth_service
from app.api import deps
from app.models.user import User

router = APIRouter()

@router.post("/register", response_model=UserResponse)
def register(user_in: UserCreate, db: Session = Depends(get_db)):
    user = auth_service.register_user(db, user_in)
    if not user:
        raise HTTPException(
            status_code=400,
            detail="The user with this username already exists in the system."
        )
    return user

@router.post("/login", response_model=Token)
def login(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    user = auth_service.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    
    return {
        "access_token": create_access_token(user.id),
        "refresh_token": create_refresh_token(user.id),
        "token_type": "bearer"
    }

@router.post("/refresh", response_model=Token)
def refresh_token(token_in: TokenRefresh, db: Session = Depends(get_db)):
    # Basic refresh validation (ideal implementation would check against DB or Redis)
    from jose import jwt, JWTError
    from app.core.config import settings
    try:
        payload = jwt.decode(token_in.refresh_token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        if payload.get("type") != "refresh":
            raise HTTPException(status_code=401, detail="Invalid token type")
        user_id = payload.get("sub")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid refresh token")
        
    return {
        "access_token": create_access_token(user_id),
        "refresh_token": token_in.refresh_token, # Send same or generate new
        "token_type": "bearer"
    }

@router.post("/logout")
def logout():
    return {"message": "Successfully logged out"}

@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(deps.get_current_active_user)):
    return current_user
