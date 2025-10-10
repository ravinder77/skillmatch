from fastapi import APIRouter, Depends, status, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from typing import Annotated, Optional, List
from app.api.dependencies import get_current_user
from app.schemas.job_application import JobApplicationResponse
from app.db.session import get_db
from app.models.user import User
from app.services import application_service

router = APIRouter()

# ----------------------------------------------------------
# Apply to a Job
# ----------------------------------------------------------
@router.post("/apply/{job_id}/", response_model=JobApplicationResponse, status_code=status.HTTP_201_CREATED)
async def apply_job(
    job_id: int,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
    resume: Optional[UploadFile] = File(None)
):
    """
      Apply to a job by providing a job ID and optional resume file.
      """
    if current_user.role.value != "candidate":
        raise HTTPException(status_code=401, detail="Not authorized to perform this action")

    application = application_service.apply_to_job(
        db=db,
        candidate_id=current_user.id,
        job_id=job_id,
        resume_file=resume
    )

    return JobApplicationResponse.model_validate(application)


# ----------------------------------------------------------
# Get All Applications by Current User
# ----------------------------------------------------------
@router.get(
    '/my',
    response_model=List[JobApplicationResponse],
    status_code=status.HTTP_200_OK
)
async def list_jobs(
        db: Annotated[Session, Depends(get_db)],
        current_user: Annotated[User, Depends(get_current_user)],
):
    """
       Fetch all job applications submitted by the current logged-in user.
       """
    if current_user.role.value != "candidate":
        raise HTTPException(
            status_code=401,
            detail="Not authorized to perform this action"
        )

    applications = application_service.get_all_applications_by_candidate(db, current_user.id)

    return applications




# ----------------------------------------------------------
# Get Application by Job ID
# ----------------------------------------------------------
@router.get('/{job_id}', response_model=JobApplicationResponse, status_code=200)
async def get_application_by_job(
    job_id: int,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],

):
    """
       Get details of a job application made by the current user for a specific job.
       """
    if current_user.role.value != "candidate":
        raise HTTPException(
            status_code=401,
            detail="Not authorized to perform this action"
        )

    application = application_service.get_application_by_job_and_candidate(db, job_id, current_user.id)
    return JobApplicationResponse.model_validate(application)
