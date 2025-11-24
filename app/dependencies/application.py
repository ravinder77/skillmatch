from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.repositories.application_repository import ApplicationRepository
from app.repositories.job_repository import JobRepository
from app.services.application_service import ApplicationService


def get_application_repository(
    db: Annotated[AsyncSession, Depends(get_db)],
) -> ApplicationRepository:
    return ApplicationRepository(db)


def get_application_service(
    db: Annotated[AsyncSession, Depends(get_db)],
) -> ApplicationService:
    app_repo = ApplicationRepository(db)
    job_repo = JobRepository(db)
    return ApplicationService(app_repo, job_repo)
