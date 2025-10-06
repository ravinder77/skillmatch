from sqlalchemy.exc import IntegrityError
from sqlalchemy import select
from fastapi import HTTPException
from sqlalchemy.orm import Session
from typing import Optional, List
from app.models.job import Job


def create(db: Session, job: Job) -> Job:
    """
    Create a job in the database
    """
    try:
        db.add(job)
        db.commit()
        db.refresh(job)
        return job
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Job with these details already exists")
    except Exception:
        db.rollback()
        raise HTTPException(status_code=500, detail="Internal Server Error while creating job")

def get_by_id(db: Session, job_id: int) -> Optional[Job]:
    """ Fetch a job by id """
    query = select(Job).where(Job.id == job_id)
    return db.execute(query).scalars().first()


def get_all(db: Session, skip: int = 0, limit: int = 10) -> List[Job]:
    """ Fetch all jobs with pagination """
    query = select(Job).offset(skip).limit(limit)
    return list(db.execute(query).scalars().all())



def update(db: Session, db_job: Job, data: dict) -> Job:
    """Update a job in the database"""
    for field, value in data.items():
        setattr(db_job, field, value)
    try:
        db.add(db_job)
        db.commit()
        db.refresh(db_job)
        return db_job
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Invalid data")
    except Exception:
        db.rollback()
        raise HTTPException(status_code=500, detail="Internal Server Error while updating job")

def delete(db: Session, job_id: int) -> bool:
    db_job = get_by_id(db, job_id)
    if not db_job:
        return False
    db.delete(db_job)
    db.commit()
    return True




