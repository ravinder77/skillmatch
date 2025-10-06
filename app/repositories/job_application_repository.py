from typing import Optional

from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError

from app.models.job import Job
from app.models.job_application import JobApplication
from sqlalchemy.orm import Session
from sqlalchemy import select

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


def get_by_candidate_and_job(db: Session, candidate_id: int, job_id: int) -> Optional[JobApplication]:
    stmt = select(JobApplication).where(
        JobApplication.candidate_id == candidate_id,
        JobApplication.job_id == job_id
    )
    return db.execute(stmt).scalar_one_or_none()