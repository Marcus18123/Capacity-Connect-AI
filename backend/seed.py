import asyncio
from sqlalchemy.orm import Session
from app.core.database import SessionLocal, engine
from app.models.base import BaseModel
from app.models.user import User, UserRole, UserStatus
from app.core.security import get_password_hash
from app.models.trainee_profile import TraineeProfile
from app.models.trainer_profile import TrainerProfile, ApprovalStatus
from app.models.competency import Competency, CompetencyLevel

def init_db(db: Session) -> None:
    # Seed 1 Admin
    admin_email = "admin@capacityconnect.com"
    if not db.query(User).filter(User.email == admin_email).first():
        admin = User(
            name="System Admin",
            email=admin_email,
            password_hash=get_password_hash("admin123"),
            role=UserRole.ADMIN,
            status=UserStatus.ACTIVE
        )
        db.add(admin)
        db.commit()

    # Seed 3 Trainees
    for i in range(1, 4):
        email = f"trainee{i}@example.com"
        if not db.query(User).filter(User.email == email).first():
            trainee = User(
                name=f"Trainee {i}",
                email=email,
                password_hash=get_password_hash("password123"),
                role=UserRole.TRAINEE,
                status=UserStatus.ACTIVE
            )
            db.add(trainee)
            db.commit()
            db.refresh(trainee)
            
            profile = TraineeProfile(
                user_id=trainee.id,
                bio=f"Bio for Trainee {i}",
                current_role="Software Engineer",
                experience_years=i*2
            )
            db.add(profile)
            db.commit()

    # Seed Competencies
    comp_name = "Data Analysis"
    if not db.query(Competency).filter(Competency.name == comp_name).first():
        comp = Competency(
            name=comp_name,
            description="Ability to analyze data",
            category="Data Science",
            level=CompetencyLevel.INTERMEDIATE
        )
        db.add(comp)
        db.commit()

    print("Database seeded successfully!")

def main() -> None:
    db = SessionLocal()
    init_db(db)

if __name__ == "__main__":
    main()
