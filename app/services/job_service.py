from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from starlette import status
from app.models.job import Job
from app.repositories.job_repository import JobRepository
from app.schemas.job import JobCreate, JobResponse


class JobService:
    def __init__(self, job_repo: JobRepository):
        self.job_repo = job_repo

    async def create_job(self, job_in: JobCreate, employer_id: int) -> JobResponse:
        if job_in.min_salary and job_in.max_salary and job_in.min_salary > job_in.max_salary:
            raise HTTPException(status_code=400, detail="min_salary cannot be greater than max_salary.")

        new_job = Job(
            title=job_in.title,
            description=job_in.description,
            skills_required=job_in.skills_required,
            experience_required=job_in.experience_required,
            min_salary=job_in.min_salary,
            max_salary=job_in.max_salary,
            location=job_in.location,
            company_id=job_in.company_id,
            employer_id=employer_id,
        )

        await self.job_repo.create(new_job)
        return JobResponse.model_validate(new_job)

    # TODO: add pagination
    async def get_all_active_jobs(self) -> List[Job]:
        jobs = await self.job_repo.get_all()
        if not jobs or len(jobs) == 0:
            raise HTTPException(
                status_code=404,
                detail="No active jobs found",
            )
        return jobs

    #
    async def get_job_by_id(self, job_id: int) -> JobResponse:
        """ Retrieve a job by its ID or raise 404 if not found. """
        job = await self.job_repo.get_by_id(job_id)
        if not job:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job not found")
        return JobResponse.model_validate(job)

    async def delete_job(self, job_id: int, employer_id) -> None:
        """ Delete a job if the employer owns it. """
        job = await self.job_repo.get_job_by_employer_id(job_id, employer_id)
        if not job or job.employer_id != employer_id:
            raise HTTPException(status_code=404, detail="Job not found.")
        await self.job_repo.delete(job_id)
        return None

    async def update_job(self, job_id: int, job_data, employer_id: int) -> Job:
        job = await self.job_repo.get_job_by_employer_id(job_id, employer_id)
        if not job:
            raise HTTPException(status_code=404, detail="Job not found.")
        if job.employer_id != employer_id:
            raise HTTPException(status_code=401, detail="You are not allowed to edit this job.")
        updated_job = await self.job_repo.update(job_id, job_data)
        return updated_job
