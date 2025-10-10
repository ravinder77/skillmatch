from typing import List

from fastapi import HTTPException
from app.models.job import Job
from app.repositories import job_repository
from app.schemas.job import JobCreate
from sqlalchemy.orm import Session

def create_job(db: Session, job_in:JobCreate, employer_id: int) -> Job:

    if job_in.min_salary > job_in.max_salary:
        raise HTTPException(status_code=400, detail="min_salary cannot be greater than max_salary.")

    new_job = Job(
        title=job_in.title,
        description=job_in.description,
        skills_required=job_in.skills_required,
        experience_required=job_in.experience_required,
        min_salary=job_in.min_salary,
        max_salary=job_in.max_salary,
        location=job_in.location,
        employer_id=employer_id,
    )

    return job_repository.create(db, new_job)

def get_all_active_jobs(db: Session) -> List[Job]:
    return job_repository.get_all(db)


def get_job_by_id(db: Session, job_id: int) -> Job:
    """ Retrieve a job by its ID or raise 404 if not found. """
    job = job_repository.get_by_id(db, job_id)

    if not job:
        raise HTTPException(status_code=404, detail="Job not found.")
    return job

def delete_job(db: Session, job_id: int, employer_id) -> None:
    """ Delete a job if the employer owns it. """
    job = job_repository.get_job_by_employer_id(db, job_id, employer_id)

    if not job or job.employer_id != employer_id:
        raise HTTPException(status_code=404, detail="Job not found.")
    job_repository.delete(db, job_id)
    return None


def update_job(db: Session, job_id: int, job_data, employer_id: int) -> Job:

    job = job_repository.get_job_by_employer_id(db, job_id, employer_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found.")
    if job.employer_id != employer_id:
        raise HTTPException(status_code=401, detail="You are not allowed to edit this job.")

    updated_job = job_repository.update(db, job_id, job_data)
    return updated_job
