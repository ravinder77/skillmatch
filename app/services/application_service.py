from typing import Optional, List
from fastapi import HTTPException
from starlette import status

from app.models.application import Application
from app.config.settings import settings
from app.repositories.application_repository import ApplicationRepository
from app.repositories.job_repository import JobRepository
from app.utils.upload_file import upload_file_to_s3


class ApplicationService:
    def __init__(self, application_repo: ApplicationRepository, job_repository: JobRepository):
        self.application_repository = application_repo
        self.job_repository = job_repository

    async def apply_to_job(
            self,
            applicant_id: int,
            job_id: int,
            resume_file: Optional = None) -> Application:
        """
          Allows a candidate (user) to apply for a job.
          Handles duplicate application checks and optional resume upload.
          """
        # Fetch Job
        job = await self.job_repository.get_by_id(job_id)
        if not job:
            raise HTTPException(status_code=404, detail="Job not found")
        if not job.is_active:
            raise HTTPException(status_code=400, detail="Not accepting application currently")

        # Check if already applied for the job
        existing_application = await self.application_repository.get_by_applicant_and_job(job_id, applicant_id)

        if existing_application:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="You have already applied for this job"
            )

        # upload resume
        resume_url: Optional[str] = None

        if resume_file:
            try:
                bucket = settings.AWS_S3_BUCKET
                file_key = upload_file_to_s3(resume_file, bucket, applicant_id)
                resume_url = f"s3://{bucket}/{file_key}"
            except Exception as e:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Resume upload failed: {str(e)}"
                )

        # Create Job Application object
        job_application = Application(
            applicant_id=applicant_id,
            job_id=job_id,
            resume_url=resume_url,
        )

        return await self.application_repository.create(job_application)

    # ----------------------------------------------------------
    # Get All Applications by a Applicant
    # ----------------------------------------------------------
    async def get_all_applications_by_applicant(self, applicant_id: int, ) -> List[Application]:
        # Fetch all applications by this user
        applications = await self.application_repository.get_all_by_applicant(applicant_id)
        return list(applications)

    # ----------------------------------------------------------
    # Get a Specific Application (by job_id and applicant_id)
    # ----------------------------------------------------------
    async def get_application_by_applicant_and_job(self, applicant_id: int, job_id: int) -> Application:
        """Fetch a job application by job ID and candidate's ID."""
        application = await self.application_repository.get_by_applicant_and_job(job_id, applicant_id)

        if not application:
            raise HTTPException(
                status_code=404,
                detail="Job application not found"
            )
        return application