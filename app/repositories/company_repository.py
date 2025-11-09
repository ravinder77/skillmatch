from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete

from app.repositories.base import BaseRepository
from app.models import Company


class CompanyRepository(BaseRepository[Company]):
    def __init__(self, db: AsyncSession):
        super().__init__(Company, db)
        self.db = db

    async def create(self, company: Company) -> Company:
        try:
            self.db.add(company)
            await self.db.commit()
            await self.db.refresh(company)
            return company
        except Exception:
            await self.db.rollback()
            raise

    async def get_by_name(self, name: str) -> Company | None:
        stmt = select(Company).where(Company.name == name)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()


    async def get_by_id(self, company_id: int) -> Company | None:
        stmt = select(Company).where(Company.id == company_id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()


    async def get_all(self) -> List[Company]:
        stmt = select(Company).order_by(Company.id.desc())
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def update(self, company: Company, company_data: dict) -> Company:
        for key, value in company_data.items():
            setattr(self, key, value)

        await self.db.commit()
        await self.db.refresh(company)
        return company

    async def delete(self, company_id: int) -> None:
        company = select(Company).where(Company.id == company_id)
        if company:
            await self.db.delete(company)
            await self.db.commit()













