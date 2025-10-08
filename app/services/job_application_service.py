from typing import Optional, List
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from starlette import status

from app.models.candidate_profile import CandidateProfile
from app.models.job import Job
from app.models.job_application import JobApplication
from app.repositories import job_application_repository
from app.core.config import settings
from app.utils.upload_file import upload_file_to_s3


async def apply_to_job(
        db: Session,
        candidate_user_id: int,
        job_id: int,
        resume_file: Optional = None
) -> JobApplication:

    candidate_profile = db.execute(
        select(CandidateProfile).where(CandidateProfile.user_id == candidate_user_id)
    ).scalar_one_or_none()

    if not candidate_profile:
        raise HTTPException(status_code=404, detail="Candidate profile not found")

    # Fetch Job
    job = db.execute(
        select(Job).where(Job.id == job_id)
    ).scalar_one_or_none()

    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    if not job.is_active:
        raise HTTPException(status_code=404, detail="Not accepting application currently")

    # Check if already applied for the job
    existing_application = job_application_repository.get_by_candidate_and_job(db, candidate_profile.id, job.id)
    if existing_application:
        raise HTTPException(status_code=400, detail="You have already applied for this job")

    # upload resume
    resume_url: Optional[str] = None
    if resume_file:
        try:
            bucket = settings.AWS_S3_BUCKET
            file_key = upload_file_to_s3(resume_file, bucket, candidate_user_id)
            resume_url = f"s3://{bucket}/{file_key}"
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Resume upload failed: {str(e)}"
            )

    # Create Job Application object
    job_application = JobApplication(
        candidate_id=candidate_profile.id,
        job_id=job_id,
        resume_url=resume_url,
    )

    return job_application_repository.create(db, job_application)


# ----------------------------------------------------------
# Get All Applications by a Candidate
# ----------------------------------------------------------
async def get_all_applications_by_user(
        db: Session,
        candidate_user_id: int,
) -> List[JobApplication]:

    candidate_profile = db.execute(
        select(CandidateProfile).where(CandidateProfile.user_id == candidate_user_id)
    ).scalar_one_or_none()

    if not candidate_profile:
        raise HTTPException(status_code=404, detail="Candidate profile not found")

    # Fetch all applications by this user
    applications = db.execute(
        select(JobApplication).where(JobApplication.candidate_id == candidate_profile.id)
    ).scalars().all()

    return list(applications)



# ----------------------------------------------------------
# Get a Specific Application (by job_id and candidate_id)
# ----------------------------------------------------------
async def get_application_by_job_and_user(
    db: Session,
    job_id: int,
    candidate_user_id: int,
)->Optional[JobApplication]:

    candidate_profile = db.execute(
        select(CandidateProfile).where(CandidateProfile.user_id == candidate_user_id)
    ).scalar_one_or_none()

    if not candidate_profile:
        raise HTTPException(
            status_code=404,
            detail="Candidate profile not found"
        )

    application = job_application_repository.get_by_candidate_and_job(db, candidate_profile.id, job_id)

    if not application:
        raise HTTPException(status_code=404, detail="Job application not found")
    return application