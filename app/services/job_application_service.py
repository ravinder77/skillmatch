from typing import Optional, List
from fastapi import HTTPException
from sqlalchemy.orm import Session
from starlette import status

from app.models.job_application import JobApplication
from app.repositories import job_application_repository, candidate_profile_repository, job_repository
from app.core.config import settings
from app.utils.upload_file import upload_file_to_s3

def apply_to_job(
        db: Session,
        user_id: int,
        job_id: int,
        resume_file: Optional = None
) -> JobApplication:

    candidate_profile = candidate_profile_repository.get_profile_by_id(db, user_id)

    if not candidate_profile:
        raise HTTPException(status_code=404, detail="Candidate profile not found")

    # Fetch Job
    job = job_repository.get_by_id(db, job_id)

    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    if not job.is_active:
        raise HTTPException(status_code=400, detail="Not accepting application currently")

    # Check if already applied for the job
    existing_application = job_application_repository.get_by_candidate_and_job(db, job_id, candidate_profile.id)
    if existing_application:
        raise HTTPException(status_code=400, detail="You have already applied for this job")

    # upload resume
    resume_url: Optional[str] = None
    if resume_file:
        try:
            bucket = settings.AWS_S3_BUCKET
            file_key = upload_file_to_s3(resume_file, bucket, user_id)
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
def get_all_applications_by_user(
        db: Session,
        user_id: int,
) -> List[JobApplication]:

    candidate_profile = candidate_profile_repository.get_profile_by_id(db, user_id)

    if not candidate_profile:
        raise HTTPException(status_code=404, detail="Candidate profile not found")

    # Fetch all applications by this user
    applications = job_application_repository.get_all_by_candidate(db, candidate_profile.id)

    return list(applications)


# ----------------------------------------------------------
# Get a Specific Application (by job_id and candidate_id)
# ----------------------------------------------------------
def get_application_by_job_and_user(
    db: Session,
    user_id: int,
    job_id: int,
) -> JobApplication:
    """
       Fetch a job application by job ID and candidate's user ID.
       Raises:
           HTTPException(404): If candidate profile or job application not found.
       """

    candidate_profile = candidate_profile_repository.get_profile_by_id(db, user_id)

    if not candidate_profile:
        raise HTTPException(
            status_code=404,
            detail="Candidate profile not found"
        )

    application = job_application_repository.get_by_candidate_and_job(db, job_id, candidate_profile.id)

    if not application:
        raise HTTPException(
            status_code=404,
            detail="Job application not found"
        )
    return application