from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException
from typing import Optional, List

from app.models.job import Job
from app.repositories.base import BaseRepository


class JobRepository(BaseRepository[Job]):
    def __init__(self, db: AsyncSession):
        super().__init__(Job, db)
        self.db = db

    async def create(self, job: Job) -> Job:
        """Create a job in the database """
        try:
            self.db.add(job)
            await self.db.commit()
            await self.db.refresh(job)
            return job
        except IntegrityError:
            await self.db.rollback()
            raise HTTPException(status_code=400, detail="Job with these details already exists")
        except Exception:
            await self.db.rollback()
            raise HTTPException(status_code=500, detail="Internal Server Error while creating job")

    async def get_by_id(self, job_id: int) -> Optional[Job]:
        """ Get a job by id """
        query = select(Job).where(Job.id == job_id)
        result = await self.db.execute(query)
        return result.scalars().first()

    async def get_all(
            self,
            page: int,
            limit: int,
            search: Optional[str],
            location: Optional[str],
            job_type: Optional[str],
            experience: Optional[str]) -> List[Job]:
        """ Fetch all jobs with pagination """
        # base query
        query = select(Job).where(Job.is_active == True)

        # --searching--
        if search:
            query = query.where(
                Job.job_type.ilike(f"%{search}%"),
            )

        # --filtering--
        if location:
            query = query.where(
                Job.location.ilike(f"%{location}%"),
            )

        if job_type:
            query = query.where(Job.job_type == job_type),

        if experience:
            query = query.where(Job.experience_required == experience),

        # --pagination--
        offset = (page - 1) * limit
        query = query.offset(offset).limit(limit)



        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def update(self, job_id: int, job_data: dict) -> Job:
        """Update a job in the database"""
        db_job = await self.get_by_id(job_id)
        if not db_job:
            raise HTTPException(status_code=404, detail="Job not found")
        for field, value in job_data.items():
            setattr(db_job, field, value)
        try:
            self.db.add(db_job)
            await self.db.commit()
            await self.db.refresh(db_job)
            return db_job
        except IntegrityError:
            await self.db.rollback()
            raise HTTPException(status_code=400, detail="Invalid data")
        except Exception:
            await self.db.rollback()
            raise HTTPException(status_code=500, detail="Internal Server Error while updating job")

    async def delete(self, job_id: int) -> bool:
        db_job = await self.get_by_id(job_id)
        if not db_job:
            return False
        await self.db.delete(db_job)
        await self.db.commit()
        return True

    async def get_job_by_employer_id(self, job_id: int, employer_id) -> Job:
        stmt = select(Job).where(
            Job.employer_id == employer_id,
            Job.id == job_id,
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()




