from fastapi import APIRouter
from app.api.v1 import auth_routes, user_routes, job_routes,application_routes

api_router = APIRouter()

api_router.include_router(auth_routes.router, prefix="/auth", tags=["auth"])
api_router.include_router(user_routes.router, prefix="/users", tags=["users"])

api_router.include_router(job_routes.router, prefix="/jobs", tags=["jobs"])

api_router.include_router(application_routes.router, prefix="/applications", tags=["Job Applications"])
