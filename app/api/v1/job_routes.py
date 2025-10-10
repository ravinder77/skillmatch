"""
Job Routes
"""
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from typing import Optional, Annotated, List
from sqlalchemy.orm import Session
from starlette import status
from app.schemas.job import JobResponse, JobCreate, JobUpdate
from app.models.user import User
from ..dependencies import get_current_employer
from app.db.session import get_db
from ...models.job import Job
from ...models.application import JobApplication
from app.services import job_service


router = APIRouter()


# ----------------------------------------------------------
# Create a Job (Recruiter/Admin only)
# ----------------------------------------------------------
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

# ----------------------------------------------------------
# Delete a Job (Recruiter/Admin only)
# ----------------------------------------------------------
@router.delete("/delete", status_code=status.HTTP_204_NO_CONTENT)
async def delete_job(
        job_id: int,
        db: Annotated[Session, Depends(get_db)],
        current_employer: Annotated[User, Depends(get_current_employer)],
):
    job_service.delete_job(db, job_id, current_employer.id)


# ----------------------------------------------------------
# Get All Active Jobs (for candidates)
# ----------------------------------------------------------
@router.get(
    "/",
    response_model=List[JobResponse],
    status_code=status.HTTP_200_OK
)
def get_all_active_jobs(
        db: Annotated[Session, Depends(get_db)]
) -> List[Job]:
    """ Retrieve all active jobs """
    jobs = get_all_active_jobs(db)
    return jobs


# ----------------------------------------------------------
# Get a Single Job by ID
# ----------------------------------------------------------
@router.get(
    "/{job_id}",
    response_model=JobResponse,
    status_code=status.HTTP_200_OK
)
def get_job_by_id(
        job_id: int,
        db: Annotated[Session, Depends(get_db)]
):
    """ Retrieve a specific job by its ID. """
    job = job_service.get_job_by_id(db, job_id)
    if not job:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job not found")
    return JobResponse.model_validate(job)

# ----------------------------------------------------------
# Update a Job
# ----------------------------------------------------------
@router.put(
    "/{job_id}",
    response_model=JobResponse,
    status_code=status.HTTP_200_OK
)
def update_job(
        job_id: int,
        job_data: JobUpdate,
        db: Annotated[Session, Depends(get_db)],
        current_employer: Annotated[User, Depends(get_current_employer)],
):
    """ Update a specific job by its ID. """
    job = job_service.update_job(db, job_id, job_data, current_employer.id)
