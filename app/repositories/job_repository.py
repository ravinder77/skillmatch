from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException

from typing import Optional, List
from app.models.job import Job


async def create(db: AsyncSession, job: Job) -> Job:
    """
    Create a job in the database
    """
    try:
        db.add(job)
        await db.commit()
        await db.refresh(job)
        return job
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=400, detail="Job with these details already exists")
    except Exception:
        await db.rollback()
        raise HTTPException(status_code=500, detail="Internal Server Error while creating job")

async def get_by_id(db: AsyncSession, job_id: int) -> Optional[Job]:
    """ Fetch a job by id """
    query = select(Job).where(Job.id == job_id)
    result = await db.execute(query)
    return result.scalars().first()


async def get_all(db: AsyncSession, skip: int = 0, limit: int = 10) -> List[Job]:
    """ Fetch all jobs with pagination """
    query = select(Job).where(Job.is_active == True).offset(skip).limit(limit)
    result = await db.execute(query)
    return list(result.scalars().all())



async def update(db: AsyncSession, job_id: int, job_data: dict) -> Job:
    """Update a job in the database"""
    db_job = await get_by_id(db, job_id)
    for field, value in job_data.items():
        setattr(db_job, field, value)
    try:
        db.add(db_job)
        await db.commit()
        await db.refresh(db_job)
        return db_job
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=400, detail="Invalid data")
    except Exception:
        await db.rollback()
        raise HTTPException(status_code=500, detail="Internal Server Error while updating job")


async def delete(db: AsyncSession, job_id: int) -> bool:
    db_job = await get_by_id(db, job_id)
    if not db_job:
        return False
    await db.delete(db_job)
    await db.commit()
    return True


async def get_job_by_employer_id(db: AsyncSession, job_id: int, employer_id) -> Job:
    stmt = select(Job).where(
        Job.employer_id == employer_id,
        Job.id == job_id,
    )
    result = await db.execute(stmt)
    return result.scalar_one_or_none()