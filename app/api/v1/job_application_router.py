from fastapi import APIRouter, Depends, status, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from typing import Annotated, Optional, List
from app.api.dependencies import get_current_user
from app.schemas.job_application import JobApplicationResponse
from app.db.session import get_db
from app.models.user import User
from app.services import job_application_service

router = APIRouter(prefix="/job-applications", tags=["Job Applications"])

@router.post("/{job_id}/apply", response_model=JobApplicationResponse, status_code=status.HTTP_201_CREATED)
async def apply_job(
    job_id: int,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
    resume: Optional[UploadFile] = File(None)
):
    if current_user.role.value != "candidate":
        raise HTTPException(status_code=401, detail="Not authorized to perform this action")

    application = job_application_service.apply_to_job(
        db=db,
        candidate_user_id=current_user.id,
        job_id=job_id,
        resume_file=resume
    )

    return JobApplicationResponse.model_validate(application)

@router.get('/', response_model=List[JobApplicationResponse], status_code=status.HTTP_200_OK)
async def list_jobs(db: Annotated[Session, Depends(get_db)]):



@router.get('/{job_id}', response_model=JobApplicationResponse, status_code=200)
async def get_job(
    job_id: int,

)