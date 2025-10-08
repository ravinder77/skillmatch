from fastapi import APIRouter
from app.api.v1 import auth_routes, projects, skill_routes, users_routes, portfolio, job_routes, candidate_profile_routes, \
    job_application_routes

api_router = APIRouter()

api_router.include_router(auth_routes.router, prefix="/auth", tags=["auth"])
api_router.include_router(users_routes.router, prefix="/users", tags=["users"])
api_router.include_router(skill_routes.router, prefix="/skills", tags=["skills"])
api_router.include_router(job_routes.router, prefix="/jobs", tags=["jobs"])

api_router.include_router(candidate_profile_routes.router, prefix="/candidate", tags=["candidate_profile"])

api_router.include_router(job_application_routes.router, prefix="/applications", tags=["Job Applications"])
