from sqlalchemy.exc import IntegrityError
from sqlalchemy import select
from sqlalchemy.orm import Session
from typing import Optional, List
from app.models.job import Job
from app.schemas.job import JobCreate, JobUpdate



def create_job(db: Session, job_in: JobCreate) -> Job:
    """
    Create a job in the database
    """
    job = Job(**job_in.model_dump())
    try:
        db.add(job)
        db.commit()
        db.refresh(job)
        return job
    except Exception as e:
        db.rollback()
        raise e

def get_job_by_id(db: Session, job_id: int) -> Optional[Job]:
    """ Fetch a job by id """
    query = select(Job).where(Job.id == job_id)
    return db.execute(query).scalars().first()


def get_jobs(db: Session, skip: int = 0, limit: int = 10) -> List[Job]:
    """ Fetch all jobs with pagination """
    query = select(Job).offset(skip).limit(limit)
    return list(db.execute(query).scalars().all())



def update_job(db: Session, db_job: Job, updates: JobUpdate) -> Job:
    """Update a job in the database"""
    for field, value in updates.model_dump(exclude_unset=True).items():
        setattr(db_job, field, value)
    try:
        db.add(db_job)
        db.commit()
        db.refresh(db_job)
        return db_job
    except IntegrityError as e:
        db.rollback()
        raise e

def delete_job(db: Session, job_id: int) -> bool:
    db_job = get_job_by_id(db, job_id)
    if not db_job:
        return False
    db.delete(db_job)
    db.commit()
    return True


