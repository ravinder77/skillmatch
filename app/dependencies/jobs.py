from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.repositories.job_repository import JobRepository
from app.services.job_service import JobService


async def get_job_repository(
    db: Annotated[AsyncSession, Depends(get_db)],
) -> JobRepository:
    return JobRepository(db)


async def get_job_service(
    repo: Annotated[JobRepository, Depends(get_job_repository)],
) -> JobService:
    return JobService(repo)
