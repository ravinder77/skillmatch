"""
Job and Job Application Routes
"""
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from typing import Optional, Annotated
from sqlalchemy.orm import Session
from starlette import status
from app.schemas.job import JobResponse, JobCreate
from app.models.user import User
from ..dependencies import get_current_employer
from app.db.session import get_db
from ...models.job import Job
from ...models.job_application import JobApplication
from app.services import job_service


router = APIRouter()

@router.post("/", response_model=JobResponse, status_code=status.HTTP_201_CREATED)
async def create_job(
        job_data: JobCreate,
        current_employer: Annotated[User, Depends(get_current_employer)],
        db: Annotated[Session, Depends(get_db)]
):
    # Authorization check
    if current_employer.role != "employer":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You are unauthorized to perform this action."
        )
    job = job_service.create_job(db, job_data, current_employer.id)
    return JobResponse.model_validate(job)

@router.delete("/delete", status_code=status.HTTP_204_NO_CONTENT)
async def delete_job(
        job_id: int,
        db: Annotated[Session, Depends(get_db)]
):

    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job not found")

    db.delete(job)
    db.commit()


@router.get("/{job_id}/candidates", status_code=status.HTTP_200_OK)
async def get_job_applications(
        job_id: int,
        db: Annotated[Session, Depends(get_db)],
        employer: Annotated[User, Depends(get_current_employer)],
):

    if employer.role.value != "employer":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authorized to perform this action"
        )

    job = db.query(Job).filter(Job.id == job_id).first()

    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found"
        )

    if employer.id != job.employer_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authorized to perform this action"
        )

    applications = (
        db.query(JobApplication)
        .filter(JobApplication.job_id == job.id)
        .all()
    )

    return applications


















