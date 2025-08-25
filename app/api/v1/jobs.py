from typing import Optional, Annotated
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status
from app.schemas.job import JobResponse, JobCreate, JobUpdate
from app.models import User, Job
from ..dependencies import get_current_user

from app.db.session import get_db

router = APIRouter()

@router.post("/post", response_model=JobResponse, status_code=status.HTTP_201_CREATED)
async def create_job(
        job_data: JobCreate,
        current_user: Annotated[User, Depends(get_current_user)],
        db: Annotated[Session, Depends(get_db)]
):

    if current_user.role != "employer":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authorized to perform this action")

    # Create New Job
    new_job = Job(**job_data.model_dump())

    #Link job to current employer
    new_job.employer_id = current_user.id

    db.add(new_job)
    db.commit()
    db.refresh(new_job)

    return new_job


