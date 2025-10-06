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




