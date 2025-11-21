from fastapi import APIRouter, Depends, HTTPException
from typing import Annotated
from starlette import status

from app.dependencies.auth import get_current_user
from app.dependencies.company import get_company_service
from app.models import User
from app.schemas.company import CompanyCreate, CompanyResponse
from app.services.company_service import CompanyService

router = APIRouter()

@router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_company(
        data: CompanyCreate,
        company_service: Annotated[CompanyService, Depends(get_company_service)],
        current_user: Annotated[User, Depends(get_current_user)],
):
    """Create a new company"""

    company = await company_service.create_company(current_user, data)
    return company


@router.get("/{company_id}", response_model=CompanyResponse, status_code=status.HTTP_200_OK)
async def get_company_by_id(
        company_id: int,
        company_service: Annotated[CompanyService, Depends(get_company_service)]
):
    """Get a company by id"""
    company = await company_service.get_company_by_id(company_id)
    return company