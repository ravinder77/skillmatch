from typing import Optional, List
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from starlette import status

from app.models.application import JobApplication
from app.repositories import application_repository, job_repository
from app.core.config import settings
from app.utils.upload_file import upload_file_to_s3

async def apply_to_job(
        db: AsyncSession,
        candidate_id: int,
        job_id: int,
        resume_file: Optional = None
) -> JobApplication:
    """
      Allows a candidate (user) to apply for a job.
      Handles duplicate application checks and optional resume upload.
      """

    # Fetch Job
    job = await job_repository.get_by_id(db, job_id)

    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    if not job.is_active:
        raise HTTPException(status_code=400, detail="Not accepting application currently")

    # Check if already applied for the job
    existing_application = await application_repository.get_by_candidate_and_job(db, job_id, candidate_id)
    if existing_application:
        raise HTTPException(status_code=400, detail="You have already applied for this job")

    # upload resume
    resume_url: Optional[str] = None
    if resume_file:
        try:
            bucket = settings.AWS_S3_BUCKET
            file_key = upload_file_to_s3(resume_file, bucket, candidate_id)
            resume_url = f"s3://{bucket}/{file_key}"
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Resume upload failed: {str(e)}"
            )

    # Create Job Application object
    job_application = JobApplication(
        candidate_id=candidate_id,
        job_id=job_id,
        resume_url=resume_url,
    )

    return await application_repository.create(db, job_application)


# ----------------------------------------------------------
# Get All Applications by a Candidate
# ----------------------------------------------------------
async def get_all_applications_by_candidate(
        db: AsyncSession,
        candidate_id: int,
) -> List[JobApplication]:


    # Fetch all applications by this user
    applications = await application_repository.get_all_by_candidate(db, candidate_id)

    return list(applications)


# ----------------------------------------------------------
# Get a Specific Application (by job_id and candidate_id)
# ----------------------------------------------------------
async def get_application_by_job_and_candidate(
    db: AsyncSession,
    candidate_id: int,
    job_id: int,
) -> JobApplication:
    """
       Fetch a job application by job ID and candidate's ID.
       Raises:
           HTTPException(404): If candidate profile or job application not found.
       """

    application = await application_repository.get_by_candidate_and_job(db, job_id, candidate_id)

    if not application:
        raise HTTPException(
            status_code=404,
            detail="Job application not found"
        )
    return application