from datetime import datetime
from typing import Optional, Annotated, List
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from starlette import status
import os
from app.schemas.job import JobResponse, JobCreate, JobUpdate
from app.models import User, Job, CandidateProfile, JobApplication
from ..dependencies import get_current_employer, get_current_user
from app.db.session import get_db
from app.utils.upload_file import upload_file_to_s3
from app.core.config import settings
from ...core.enums import ApplicationStatus
from ...schemas.application import JobApplicationCreate

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



@router.post("/jobs/{job_id}/apply",  status_code=status.HTTP_201_CREATED)
async def apply_job(
        job_id: int,
        db: Annotated[Session, Depends(get_db)],
        current_user: Annotated[User, Depends(get_current_user)],
        resume: UploadFile = File(None)
):

    if current_user.role != "candidate":
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

    if not candidate_profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="You must create a candidate profile first"
        )

    #check job exists
    posted_job =  db.query(Job).filter(Job.id==job_id).first()

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

    # upload resume
    resume_url = None
    if resume:
        bucket = settings.AWS_S3_BUCKET
        file_key = upload_file_to_s3(resume, bucket, current_user.id)
        resume_url = f"s3://{bucket}/{file_key}"
    else:
        resume_url = candidate_profile.resume_url

    print(type(candidate_profile.id), candidate_profile.id)
    print(type(posted_job.id), posted_job.id)

    application = JobApplication(
        candidate_id=candidate_profile.id,
        job_id=posted_job.id,
        resume_url=resume_url,
        status=ApplicationStatus.APPLIED.value,
        applied_at=datetime.now()
    )

    db.add(application)
    db.commit()
    db.refresh(application)

    return {
        "message": "Job successfully applied",
        "application_id": application.id,
        "status": application.status,
        "resume_url": application.resume_url,
    }
















