from typing import List, Optional

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.application import Application
from app.repositories.base import BaseRepository


class ApplicationRepository(BaseRepository[Application]):
    def __init__(self, db: AsyncSession):
        super().__init__(Application, db)
        self.db = db

    # ----------------------------------------------------------
    # Create a New Job Application
    # ----------------------------------------------------------
    async def create(self, application: Application) -> Application:
        """Create a new job application"""
        try:
            self.db.add(application)
            await self.db.commit()
            await self.db.refresh(application)
            return application
        except IntegrityError:
            await self.db.rollback()
            raise HTTPException(
                status_code=400, detail="You have already applied for this job"
            )
        except Exception:
            await self.db.rollback()
            raise HTTPException(
                status_code=500, detail="Internal Server Error while updating job"
            )

    # ----------------------------------------------------------
    # Get Job Application by Applicant & Job
    # ----------------------------------------------------------
    async def get_by_applicant_and_job(
        self, applicant_id: int, job_id: int
    ) -> Optional[Application]:
        stmt = select(Application).where(
            Application.applicant_id == applicant_id, Application.job_id == job_id
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    # ----------------------------------------------------------
    # Get All Applications for a Applicant
    # ----------------------------------------------------------
    async def get_all_by_applicant(self, applicant_id: int) -> List[Application]:
        """Returns all job applications submitted by a given user."""
        stmt = select(Application).where(Application.applicant == applicant_id)
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    # ----------------------------------------------------------
    # Get All Applications for a Specific Job
    # ----------------------------------------------------------
    async def get_all_by_job(self, job_id: int) -> List[Application]:
        """Returns all job applications for a job."""
        stmt = select(Application).where(Application.job_id == job_id)
        result = await self.db.execute(stmt)
        return list(result.scalars().all())
