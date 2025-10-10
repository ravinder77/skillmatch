from typing import Optional, List
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from app.models.application import JobApplication
from sqlalchemy.orm import Session
from sqlalchemy import select


# ----------------------------------------------------------
# Create a New Job Application
# ----------------------------------------------------------
def create(db: Session, application: JobApplication) -> JobApplication:
    """ Create a new job application """
    try:
        db.add(application)
        db.commit()
        db.refresh(application)
        return application
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="You have already applied for this job")
    except Exception:
        db.rollback()
        raise HTTPException(status_code=500, detail="Internal Server Error while updating job")

# ----------------------------------------------------------
# Get Job Application by Candidate & Job
# ----------------------------------------------------------
def get_by_candidate_and_job(
        db: Session,
        job_id: int,
        candidate_id: int,
) -> Optional[JobApplication]:
    stmt = select(JobApplication).where(
        JobApplication.candidate_id == candidate_id,
        JobApplication.job_id == job_id
    )
    return db.execute(stmt).scalar_one_or_none()


# ----------------------------------------------------------
# Get All Applications for a Candidate
# ----------------------------------------------------------
def get_all_by_candidate(
    db: Session,
    candidate_id: int
) -> List[JobApplication]:
    """ Returns all job applications submitted by a given user. """
    result = db.execute(select(JobApplication).where(JobApplication.candidate_id == candidate_id))
    return list(result.scalars().all())

# ----------------------------------------------------------
# Get All Applications for a Specific Job
# ----------------------------------------------------------
def get_all_by_job(
    db: Session,
    job_id: int
) -> List[JobApplication]:
    return list(db.execute(
        select(JobApplication)
        .where(JobApplication.job_id == job_id)
    ).scalars().all())

