from typing import List

from fastapi import HTTPException

from app.models import Company
from app.repositories.company_repository import CompanyRepository
from app.schemas.company import CompanyCreate, CompanyUpdate


class CompanyService:
    def __init__(self, repo: CompanyRepository):
        self.company_repo = repo

    async def create_company(self, company_data: CompanyCreate) -> Company:
        existing_company = self.company_repo.get_by_name(company_data.company_name)
        if existing_company:
            raise HTTPException(
                status_code=400,
                detail=f"Company with name {company_data.name} already exists")

        company = Company(
            name=company_data.name,
            description=company_data.description,
            website=str(company_data.website),
            location=company_data.location,
            logo_url=str(company_data.logo_url),
            size=company_data.size,
            industry=company_data.industry
        )
        return await self.company_repo.create(company)

    async def get_company_by_id(self, company_id: int) -> Company:
        company = await self.company_repo.get_by_id(company_id)
        if not company:
            raise HTTPException(
                status_code=404,
                detail=f"Company with id {company_id} does not exist"
            )
        return company

    async def get_all_companies(self) -> List[Company]:
        """Get all companies"""
        companies = await self.company_repo.get_all()
        return companies

    async def update_company(self, company_id: int, company_data: CompanyUpdate) -> Company:
        """Update company """
        # check if a company exist
        existing_company = await self.company_repo.get_by_id(company_id)
        if not existing_company:
            raise HTTPException(
                status_code=404,
                detail=f"Company does not exist"
            )
        # pass only those fields which are provided by user
        updates = company_data.model_dump(exclude_unset=True)
        return await self.company_repo.update(existing_company, updates)
