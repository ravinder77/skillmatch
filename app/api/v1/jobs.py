from typing import Annotated, List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from starlette import status

from app.core.enums import UserRole
from app.dependencies.auth import get_current_employer
from app.dependencies.jobs import get_job_service
from app.models.user import User
from app.schemas.job import JobCreate, JobResponse, JobUpdate
from app.services.job_service import JobService

router = APIRouter()


# ----------------------------------------------------------
# Create a Job (Recruiter/Admin only)
# ----------------------------------------------------------
@router.post("/", response_model=JobResponse, status_code=status.HTTP_201_CREATED)
async def create_job(
    job_data: JobCreate,
    current_employer: Annotated[User, Depends(get_current_employer)],
    service: Annotated[JobService, Depends(get_job_service)],
):
    # Authorization check
    if current_employer.role != UserRole.EMPLOYER:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You are unauthorized to perform this action.",
        )
    job = await service.create_job(job_data, current_employer.id)
    return JobResponse.model_validate(job)


# ----------------------------------------------------------
# Delete a Job (Recruiter/Admin only)
# ----------------------------------------------------------
@router.delete("/delete", status_code=status.HTTP_204_NO_CONTENT)
async def delete_job(
    job_id: int,
    current_employer: Annotated[User, Depends(get_current_employer)],
    service: Annotated[JobService, Depends(get_job_service)],
):
    await service.delete_job(job_id, current_employer.id)
    return {"message": "Job deleted successfully."}


# ----------------------------------------------------------
# Get All Active Jobs (pagination, filtering, searching)
# ----------------------------------------------------------
@router.get("/", response_model=List[JobResponse], status_code=status.HTTP_200_OK)
async def get_all_active_jobs(
    service: Annotated[JobService, Depends(get_job_service)],
    page: int = Query(1, ge=0),
    limit: int = Query(10, ge=1, le=100),
    search: Optional[str] = Query(None),
    location: Optional[str] = Query(None),
    job_type: Optional[str] = Query(None),
):
    """Retrieve all active jobs"""
    jobs = await service.get_all_active_jobs(
        page=page, limit=limit, search=search, location=location, job_type=job_type
    )
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
    service: Annotated[JobService, Depends(get_job_service)],
):
    """Retrieve a specific job by its ID."""
    job = await service.get_job_by_id(job_id)
    job_schema = JobResponse.model_validate(job).model_dump()
    return job_schema


# ----------------------------------------------------------
# Update a Job
# ----------------------------------------------------------
@router.put("/{job_id}", response_model=JobResponse, status_code=status.HTTP_200_OK)
async def update_job(
    job_id: int,
    job_data: JobUpdate,
    service: Annotated[JobService, Depends(get_job_service)],
    current_employer: Annotated[User, Depends(get_current_employer)],
):
    """Update a specific job by its ID."""
    job = await service.update_job(job_id, job_data, current_employer.id)
    return JobResponse.model_validate(job)
