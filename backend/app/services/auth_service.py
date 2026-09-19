from sqlalchemy.orm import Session
from app.schemas.user import UserCreate
from app.repositories import user_repository
from app.core.security import verify_password
from app.models.user import UserStatus, UserRole
from app.models.trainee_profile import TraineeProfile
from app.models.trainer_profile import TrainerProfile

def register_user(db: Session, user_in: UserCreate):
    existing_user = user_repository.user.get_by_email(db, email=user_in.email)
    if existing_user:
        return None

    db_user = user_repository.user.create(db, obj_in=user_in)

    if user_in.role == UserRole.TRAINEE:
        db_user.status = UserStatus.ACTIVE
        db.add(TraineeProfile(user_id=db_user.id))
    elif user_in.role == UserRole.TRAINER:
        db_user.status = UserStatus.PENDING
        db.add(TrainerProfile(user_id=db_user.id))

    db.commit()
    db.refresh(db_user)
    return db_user

def authenticate_user(db: Session, email: str, password: str):
    user = user_repository.user.get_by_email(db, email=email)
    if not user:
        return None
    if not verify_password(password, user.password_hash):
        return None
    if user.status != UserStatus.ACTIVE:
        return None
    return user