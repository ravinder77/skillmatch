from typing import Optional, Annotated, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status
from app.schemas.job import JobResponse, JobCreate, JobUpdate
from app.models import User, Job
from ..dependencies import get_current_employer

from app.db.session import get_db

router = APIRouter()

@router.post("/post", response_model=JobResponse, status_code=status.HTTP_201_CREATED)
async def create_job(
        job_data: JobCreate,
        current_employer: Annotated[User, Depends(get_current_employer)],
        db: Annotated[Session, Depends(get_db)]
):

    # Create New Job
    new_job = Job(
        title=job_data.title,
        description=job_data.description,
        skills_required=job_data.skills_required,
        experience_required=job_data.experience_required,
        location=job_data.location,
        employer_id=current_employer.id,
    )

    db.add(new_job)
    db.commit()
    db.refresh(new_job)

    return new_job


@router.delete("/delete", status_code=status.HTTP_204_NO_CONTENT)
async def delete_job(
        job_id: int,
        current_user: Annotated[User, Depends(get_current_employer)],
        db: Annotated[Session, Depends(get_db)]
):
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job not found")

    db.delete(job)
    db.commit()


@router.get("/jobs", response_model=List[JobResponse])
async def read_jobs_by_employer(
        current_employer: Annotated[User, Depends(get_current_employer)],
        db: Annotated[Session, Depends(get_db)]
):
    """
    Retrieve all jobs associated with employer
    """
    jobs = db.query(Job).filter(Job.employer_id == current_employer.id).all()

    return jobs




