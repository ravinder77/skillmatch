from fastapi import APIRouter
from typing import List
from app.api.v1 import auth, projects, skills, users, portfolio, jobs, candidate_profile, employer

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(skills.router, prefix="/skills", tags=["skills"])
api_router.include_router(jobs.router, prefix="/jobs", tags=["jobs"])

api_router.include_router(candidate_profile.router, prefix="/candidate", tags=["candidate_profile"])

api_router.include_router(employer.router, prefix="/employer", tags=["employer"])
