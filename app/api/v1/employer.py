from typing import List, Annotated

from fastapi import APIRouter , Depends, HTTPException
from starlette import status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.api.dependencies import get_current_employer
from app.schemas.job import JobResponse
from app.models import User, Job




router = APIRouter()



@router.get("/jobs", response_model=List[JobResponse])
async def get_jobs_by_employer(
        current_employer: Annotated[User, Depends(get_current_employer)],
        db: Annotated[Session, Depends(get_db)]
):
    """
    Retrieve all jobs associated with employer
    """
    jobs = db.query(Job).filter(Job.employer_id == current_employer.id).all()

    return jobs
