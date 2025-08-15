from fastapi import APIRouter
from app.api.v1 import users, auth, skills, projects

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["auth"])