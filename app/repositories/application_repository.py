from typing import Optional, List
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.application import Application
from sqlalchemy import select


# ----------------------------------------------------------
# Create a New Job Application
# ----------------------------------------------------------
async def create(db: AsyncSession, application: Application) -> Application:
    """ Create a new job application """
    try:
        db.add(application)
        await db.commit()
        await db.refresh(application)
        return application
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=400, detail="You have already applied for this job")
    except Exception:
        await db.rollback()
        raise HTTPException(status_code=500, detail="Internal Server Error while updating job")

# ----------------------------------------------------------
# Get Job Application by Candidate & Job
# ----------------------------------------------------------
async def get_by_candidate_and_job(
        db: AsyncSession,
        job_id: int,
        candidate_id: int,
) -> Optional[Application]:
    stmt = select(Application).where(
        Application.candidate_id == candidate_id,
        Application.job_id == job_id
    )
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


# ----------------------------------------------------------
# Get All Applications for a Candidate
# ----------------------------------------------------------
async def get_all_by_candidate(
    db: AsyncSession,
    candidate_id: int
) -> List[Application]:
    """ Returns all job applications submitted by a given user. """
    stmt = select(Application).where(Application.candidate_id == candidate_id)
    result = await db.execute(stmt)
    return list(result.scalars().all())

# ----------------------------------------------------------
# Get All Applications for a Specific Job
# ----------------------------------------------------------
async def get_all_by_job(
    db: AsyncSession,
    job_id: int
) -> List[Application]:
    """ Returns all job applications for a job. """
    stmt = select(Application).where(Application.job_id == job_id)
    result = await db.execute(stmt)
    return list(result.scalars().all())

