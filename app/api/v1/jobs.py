"""
Job and Job Application Routes
"""
from datetime import datetime
from typing import Optional, Annotated
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from starlette import status
from app.schemas.job import JobResponse, JobCreate
from app.models import User, Job, CandidateProfile, JobApplication
from ..dependencies import get_current_employer, get_current_user
from app.db.session import get_db
from app.utils.upload_file import upload_file_to_s3
from app.core.config import settings
from ...core.enums import ApplicationStatus

from ...schemas.application import CandidateApplication, JobApplicationResponse
from ...services.parser_service import extract_text_from_resume

router = APIRouter()

@router.post("/", response_model=JobResponse, status_code=status.HTTP_201_CREATED)
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
        min_salary=job_data.min_salary,
        max_salary=job_data.max_salary,
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
        db: Annotated[Session, Depends(get_db)]
):

    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job not found")

    db.delete(job)
    db.commit()



# ===============
# Candidate Route
# ===============
@router.post("/{job_id}/apply", response_model=JobApplicationResponse,  status_code=status.HTTP_201_CREATED)
async def apply_job(
        job_id: int,
        db: Annotated[Session, Depends(get_db)],
        current_user: Annotated[User, Depends(get_current_user)],
        resume: UploadFile = File(None)
):

    if current_user.role.value != "candidate":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authorized to perform this action"
        )



    # check candidate profile exist
    candidate_profile = (
        db.query(CandidateProfile)
        .filter(CandidateProfile.user_id == current_user.id)
        .first()
    )

    #check job exists
    posted_job = db.query(Job).filter(Job.id == job_id).first()

    if not posted_job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found"
        )

    # check if job currently accepting application
    if not posted_job.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Not accepting applications"
        )

    # check if you already applied for the job
    existing_application =(
        db.query(JobApplication)
        .filter(JobApplication.candidate_id == candidate_profile.id,
        JobApplication.job_id == posted_job.id
    ).first()
    )

    if existing_application:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You have already applied for this job"
        )


    #upload Resume and Parse it
    parsed_text = extract_text_from_resume(resume)



    # upload resume
    resume_url: Optional[str] = None
    if resume:
        try:
            bucket = settings.AWS_S3_BUCKET
            file_key = upload_file_to_s3(resume, bucket, current_user.id)
            resume_url = f"s3://{bucket}/{file_key}"
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Resume upload failed: {str(e)}"
            )

    # Create Job Application
    application = JobApplication(
        candidate_id=candidate_profile.id,
        job_id=posted_job.id,
        resume_url=resume_url,
        status=ApplicationStatus.APPLIED.value,
        applied_at=datetime.now()
    )

    try:
        db.add(application)
        db.commit()
        db.refresh(application)
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to apply application: {str(e)}"
        )


    return JobApplicationResponse(
        message= "Job applied Successfully",
        id=application.id,
        status=application.status,
        resume_url=application.resume_url,
        applied_at=datetime.now()

    )



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


















