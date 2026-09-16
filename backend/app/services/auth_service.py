from sqlalchemy.orm import Session
from app.schemas.user import UserCreate
from app.repositories import user_repository
from app.core.security import get_password_hash, verify_password
from app.models.user import UserStatus, UserRole
from app.models.trainee_profile import TraineeProfile
from app.models.trainer_profile import TrainerProfile

def register_user(db: Session, user_in: UserCreate):
    existing_user = user_repository.user.get_by_email(db, email=user_in.email)
    if existing_user:
        return None

    status = UserStatus.PENDING
    if user_in.role == UserRole.TRAINEE:
        status = UserStatus.ACTIVE

    hashed_password = get_password_hash(user_in.password)
    
    db_user = user_repository.user.create(
        db, 
        obj_in=UserCreate(
            name=user_in.name,
            email=user_in.email,
            role=user_in.role,
            password=hashed_password # This replaces the plain password
        )
    )
    
    # Force override the hash and status since user_in schema has plain password
    db_user.password_hash = hashed_password
    db_user.status = status
    db.add(db_user)

    if user_in.role == UserRole.TRAINEE:
        profile = TraineeProfile(user_id=db_user.id)
        db.add(profile)
    elif user_in.role == UserRole.TRAINER:
        profile = TrainerProfile(user_id=db_user.id)
        db.add(profile)
        
    db.commit()
    db.refresh(db_user)
    return db_user

def authenticate_user(db: Session, email: str, password: str):
    user = user_repository.user.get_by_email(db, email=email)
    if not user:
        return None
    if not verify_password(password, user.password_hash):
        return None
    return user
