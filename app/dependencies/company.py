from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.repositories.company_repository import CompanyRepository
from app.repositories.user_repository import UserRepository
from app.services.company_service import CompanyService


def get_company_service(db: Annotated[AsyncSession, Depends(get_db)]):
    company_repository = CompanyRepository(db)
    user_repository = UserRepository(db)
    return CompanyService(company_repo=company_repository, user_repo=user_repository)
