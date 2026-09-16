import asyncio
from logging.config import fileConfig
from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config
from alembic import context
import os
import sys

# Add backend directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from app.core.config import settings
from app.models.base import BaseModel
# Import all models to ensure they are registered with BaseModel.metadata
from app.models.user import User
from app.models.trainee_profile import TraineeProfile
from app.models.trainer_profile import TrainerProfile
from app.models.competency import Competency
from app.models.user_competency import UserCompetency
from app.models.trainer_expertise import TrainerExpertise
from app.models.course import Course
from app.models.course_competency import CourseCompetency
from app.models.enrollment import Enrollment
from app.models.assessment import Assessment
from app.models.question import Question
from app.models.assessment_result import AssessmentResult
from app.models.project import Project
from app.models.submission import Submission
from app.models.learning_path import LearningPath
from app.models.learning_path_item import LearningPathItem
from app.models.skill_gap import SkillGap
from app.models.notification import Notification

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = BaseModel.metadata

def run_migrations_offline() -> None:
    url = settings.DATABASE_URL
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    from sqlalchemy import create_engine
    connectable = create_engine(settings.DATABASE_URL)

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
