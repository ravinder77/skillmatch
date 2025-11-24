from typing import List

from fastapi import HTTPException

from app.models import Company, User
from app.repositories.company_repository import CompanyRepository
from app.repositories.user_repository import UserRepository
from app.schemas.company import CompanyCreate, CompanyUpdate


class CompanyService:
    def __init__(self, company_repo: CompanyRepository, user_repo: UserRepository):
        self.company_repo = company_repo
        self.user_repo = user_repo

    async def create_company(self, user: User, data: CompanyCreate) -> Company:

        # normalize name before saving to database
        normalized_name = data.name.strip().lower()

        existing_company = await self.company_repo.get_by_name(normalized_name)
        if existing_company:
            raise HTTPException(
                status_code=400, detail=f"Company with name {data.name} already exists"
            )

        company = Company(
            name=normalized_name,
            description=data.description,
            website=str(data.website) if data.website is not None else None,
            location=str(data.location),
            logo_url=str(data.logo_url) if data.logo_url is not None else None,
            size=data.size,
            industry=data.industry,
            owner_id=user.id,
        )

        return await self.company_repo.create(company)

    async def get_company_by_id(self, company_id: int) -> Company:
        company = await self.company_repo.get_by_id(company_id)
        if not company:
            raise HTTPException(
                status_code=404, detail=f"Company with id {company_id} does not exist"
            )
        return company

    # TODO: Add Pagination
    async def get_all_companies(self) -> List[Company]:
        """Get all companies"""
        companies = await self.company_repo.get_all()
        return companies

    async def update_company(
        self, company_id: int, company_data: CompanyUpdate
    ) -> Company:
        """Update company"""
        # check if a company exist
        existing_company = await self.company_repo.get_by_id(company_id)
        if not existing_company:
            raise HTTPException(status_code=404, detail=f"Company does not exist")
        # pass only those fields which are provided by user
        updates = company_data.model_dump(exclude_unset=True)
        return await self.company_repo.update(existing_company, updates)
