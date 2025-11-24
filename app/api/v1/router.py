from fastapi import APIRouter

from app.api.v1 import applications, auth, companies, jobs, users

router = APIRouter()

router.include_router(auth.router, prefix="/auth", tags=["Auth"])
router.include_router(users.router, prefix="/users", tags=["Users"])
router.include_router(jobs.router, prefix="/jobs", tags=["Jobs"])
router.include_router(
    applications.router, prefix="/applications", tags=["Job Applications"]
)
router.include_router(companies.router, prefix="/companies", tags=["Company"])
