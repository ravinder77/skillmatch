from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated, List
from starlette import status
from app.schemas.job import JobResponse, JobCreate, JobUpdate
from app.models.user import User
from app.dependencies.auth import get_current_employer
from app.db.session import get_db
from ...core.enums import UserRole
from app.services import job_service



router = APIRouter()

# ----------------------------------------------------------
# Create a Job (Recruiter/Admin only)
# ----------------------------------------------------------
@router.post("/", response_model=JobResponse, status_code=status.HTTP_201_CREATED)
async def create_job(
        job_data: JobCreate,
        current_employer: Annotated[User, Depends(get_current_employer)],
        db: Annotated[AsyncSession, Depends(get_db)]
):
    # Authorization check
    if current_employer.role != UserRole.EMPLOYER:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You are unauthorized to perform this action."
        )
    job = await job_service.create_job(db, job_data, current_employer.id)
    return JobResponse.model_validate(job)

# ----------------------------------------------------------
# Delete a Job (Recruiter/Admin only)
# ----------------------------------------------------------
@router.delete("/delete", status_code=status.HTTP_204_NO_CONTENT)
async def delete_job(
        job_id: int,
        db: Annotated[AsyncSession, Depends(get_db)],
        current_employer: Annotated[User, Depends(get_current_employer)],
):
    await job_service.delete_job(db, job_id, current_employer.id)

    return {
        "message": "Job deleted successfully."
    }


# ----------------------------------------------------------
# Get All Active Jobs (for candidates)
# ----------------------------------------------------------
@router.get(
    "/",
    response_model=List[JobResponse],
    status_code=status.HTTP_200_OK
)
async def get_all_active_jobs(
        db: Annotated[AsyncSession, Depends(get_db)],
):
    """ Retrieve all active jobs """

    jobs = await job_service.get_all_active_jobs(db)
    jobs_list = [JobResponse.model_validate(job).model_dump() for job in jobs]

    return jobs_list


# ----------------------------------------------------------
# Get a Single Job by ID
# ----------------------------------------------------------
@router.get(
    "/{job_id}",
    response_model=JobResponse,
    status_code=status.HTTP_200_OK,
)
async def get_job_by_id(
        job_id: int,
        db: Annotated[AsyncSession, Depends(get_db)],
):
    """ Retrieve a specific job by its ID. """

    job = await job_service.get_job_by_id(db, job_id)
    job_schema = JobResponse.model_validate(job).model_dump()
    # set cache
    return job_schema

# ----------------------------------------------------------
# Update a Job
# ----------------------------------------------------------
@router.put(
    "/{job_id}",
    response_model=JobResponse,
    status_code=status.HTTP_200_OK
)
async def update_job(
        job_id: int,
        job_data: JobUpdate,
        db: Annotated[AsyncSession, Depends(get_db)],
        current_employer: Annotated[User, Depends(get_current_employer)],
):
    """ Update a specific job by its ID. """
    job = await job_service.update_job(db, job_id, job_data, current_employer.id)
    return JobResponse.model_validate(job)

