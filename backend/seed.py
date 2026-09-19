from sqlalchemy.orm import Session
from app.core.database import SessionLocal, engine
from app.models.base import Base
import app.models
from app.models.user import User, UserRole, UserStatus
from app.core.security import get_password_hash
from app.models.trainee_profile import TraineeProfile
from app.models.trainer_profile import TrainerProfile, ApprovalStatus
from app.models.competency import Competency, CompetencyLevel
from app.models.role import Role, RoleCompetency
from app.models.user_competency import UserCompetency, VerificationStatus, EvidenceSource
from app.models.trainer_expertise import TrainerExpertise


def init_db(db: Session) -> None:
    # Ensure tables are created
    Base.metadata.create_all(bind=engine)

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
                experience_years=i * 2
            )

            db.add(profile)
            db.commit()

    # Seed Trainer
    trainer_email = "trainer@capacityconnect.com"

    trainer = db.query(User).filter(
        User.email == trainer_email
    ).first()

    if not trainer:
        trainer = User(
            name="Data Analytics Trainer",
            email=trainer_email,
            password_hash=get_password_hash("trainer123"),
            role=UserRole.TRAINER,
            status=UserStatus.ACTIVE
        )

        db.add(trainer)
        db.commit()
        db.refresh(trainer)

        trainer_profile = TrainerProfile(
            user_id=trainer.id,
            professional_title="Senior Data Analytics Trainer",
            bio="Trainer specializing in Python, SQL and Data Analysis.",
            organization="Capacity Connect AI",
            experience_years=8,
            availability="Weekdays",
            languages="English",
            approval_status=ApprovalStatus.APPROVED
        )

        db.add(trainer_profile)
        db.commit()

    # Seed Competencies
    comp_name = "Data Analysis"

    if not db.query(Competency).filter(
        Competency.name == comp_name
    ).first():
        comp = Competency(
            name="Data Analysis",
            description="Ability to analyze data",
            category="Data Science",
            level=CompetencyLevel.INTERMEDIATE
        )

        db.add(comp)

    if not db.query(Competency).filter(
        Competency.name == "Python"
    ).first():
        comp_python = Competency(
            name="Python",
            description="Python programming language",
            category="Software Development",
            level=CompetencyLevel.ADVANCED
        )

        db.add(comp_python)

    if not db.query(Competency).filter(
        Competency.name == "SQL"
    ).first():
        comp_sql = Competency(
            name="SQL",
            description="Structured Query Language",
            category="Database",
            level=CompetencyLevel.ADVANCED
        )

        db.add(comp_sql)

    db.commit()

    # Get Competencies
    python_comp = db.query(Competency).filter(
        Competency.name == "Python"
    ).first()

    sql_comp = db.query(Competency).filter(
        Competency.name == "SQL"
    ).first()

    data_analysis_comp = db.query(Competency).filter(
        Competency.name == "Data Analysis"
    ).first()

    # Seed Target Role
    role_name = "Data Analyst"

    da_role = db.query(Role).filter(
        Role.name == role_name
    ).first()

    if not da_role:
        da_role = Role(
            name="Data Analyst",
            description="Analyzes data and generates insights.",
            industry="Technology",
            is_active=True
        )

        db.add(da_role)
        db.commit()
        db.refresh(da_role)

    # Seed Role Competencies
    if da_role and python_comp:
        existing = db.query(RoleCompetency).filter(
            RoleCompetency.role_id == da_role.id,
            RoleCompetency.competency_id == python_comp.id
        ).first()

        if not existing:
            db.add(
                RoleCompetency(
                    role_id=da_role.id,
                    competency_id=python_comp.id,
                    required_level=3.0,
                    importance=1.5
                )
            )

    if da_role and sql_comp:
        existing = db.query(RoleCompetency).filter(
            RoleCompetency.role_id == da_role.id,
            RoleCompetency.competency_id == sql_comp.id
        ).first()

        if not existing:
            db.add(
                RoleCompetency(
                    role_id=da_role.id,
                    competency_id=sql_comp.id,
                    required_level=3.0,
                    importance=1.2
                )
            )

    db.commit()

    # Seed User Competencies
    trainees = db.query(User).filter(
        User.role == UserRole.TRAINEE
    ).all()

    for trainee in trainees:
        if python_comp and not db.query(UserCompetency).filter(
            UserCompetency.user_id == trainee.id,
            UserCompetency.competency_id == python_comp.id
        ).first():
            db.add(
                UserCompetency(
                    user_id=trainee.id,
                    competency_id=python_comp.id,
                    proficiency_level=3.0,
                    verification_status=VerificationStatus.VERIFIED,
                    evidence_source=EvidenceSource.ASSESSMENT,
                    confidence=0.90
                )
            )

        if sql_comp and not db.query(UserCompetency).filter(
            UserCompetency.user_id == trainee.id,
            UserCompetency.competency_id == sql_comp.id
        ).first():
            db.add(
                UserCompetency(
                    user_id=trainee.id,
                    competency_id=sql_comp.id,
                    proficiency_level=2.0,
                    verification_status=VerificationStatus.ASSESSED,
                    evidence_source=EvidenceSource.ASSESSMENT,
                    confidence=0.80
                )
            )

        if data_analysis_comp and not db.query(UserCompetency).filter(
            UserCompetency.user_id == trainee.id,
            UserCompetency.competency_id == data_analysis_comp.id
        ).first():
            db.add(
                UserCompetency(
                    user_id=trainee.id,
                    competency_id=data_analysis_comp.id,
                    proficiency_level=1.0,
                    verification_status=VerificationStatus.LEARNING,
                    evidence_source=EvidenceSource.SELF_REPORTED,
                    confidence=0.60
                )
            )

    db.commit()

    # Seed Trainer Expertise
    trainer = db.query(User).filter(
        User.email == trainer_email
    ).first()

    if trainer:
        if python_comp and not db.query(TrainerExpertise).filter(
            TrainerExpertise.trainer_id == trainer.id,
            TrainerExpertise.competency_id == python_comp.id
        ).first():
            db.add(
                TrainerExpertise(
                    trainer_id=trainer.id,
                    competency_id=python_comp.id,
                    proficiency_level=5.0,
                    years_experience=8,
                    verification_status=VerificationStatus.VERIFIED
                )
            )

        if sql_comp and not db.query(TrainerExpertise).filter(
            TrainerExpertise.trainer_id == trainer.id,
            TrainerExpertise.competency_id == sql_comp.id
        ).first():
            db.add(
                TrainerExpertise(
                    trainer_id=trainer.id,
                    competency_id=sql_comp.id,
                    proficiency_level=5.0,
                    years_experience=8,
                    verification_status=VerificationStatus.VERIFIED
                )
            )

        if data_analysis_comp and not db.query(TrainerExpertise).filter(
            TrainerExpertise.trainer_id == trainer.id,
            TrainerExpertise.competency_id == data_analysis_comp.id
        ).first():
            db.add(
                TrainerExpertise(
                    trainer_id=trainer.id,
                    competency_id=data_analysis_comp.id,
                    proficiency_level=5.0,
                    years_experience=8,
                    verification_status=VerificationStatus.VERIFIED
                )
            )

        db.commit()

    # Seed Sample Assessment & Questions
    from app.models.assessment import Assessment, AssessmentStatus
    from app.models.question import Question, QuestionType

    assessment = db.query(Assessment).filter(Assessment.title == "Data Analyst & SQL Foundations").first()
    if not assessment:
        assessment = Assessment(
            title="Data Analyst & SQL Foundations",
            description="Evaluates your mastery of SQL querying, data manipulation, and analytical reasoning.",
            duration_minutes=20,
            passing_score=70,
            status=AssessmentStatus.PUBLISHED
        )
        db.add(assessment)
        db.commit()
        db.refresh(assessment)

        q1 = Question(
            assessment_id=assessment.id,
            competency_id=sql_comp.id if sql_comp else None,
            question_text="Which SQL keyword is used to eliminate duplicate rows from a result set?",
            question_type=QuestionType.MCQ,
            difficulty="BEGINNER",
            options=["UNIQUE", "DISTINCT", "FILTER", "GROUP BY"],
            correct_answer="DISTINCT",
            explanation="DISTINCT filters out duplicate records from query results.",
            marks=1,
            order_index=1
        )
        q2 = Question(
            assessment_id=assessment.id,
            competency_id=python_comp.id if python_comp else None,
            question_text="In Python Pandas, which method is used to aggregate data based on grouping key?",
            question_type=QuestionType.MCQ,
            difficulty="INTERMEDIATE",
            options=["pivot()", "groupby()", "aggregate()", "filter()"],
            correct_answer="groupby()",
            explanation="groupby() splits the data into groups for computation.",
            marks=1,
            order_index=2
        )
        db.add_all([q1, q2])
        db.commit()

    print("Database seeded successfully!")



def main() -> None:
    db = SessionLocal()

    try:
        init_db(db)
    finally:
        db.close()


if __name__ == "__main__":
    main()