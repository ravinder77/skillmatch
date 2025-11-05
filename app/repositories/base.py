from typing import Generic, TypeVar, Type, List, Optional, Protocol

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.base import Base

ModelType = TypeVar('ModelType', bound=Base)

class BaseRepository(Generic[ModelType]):

    def __init__(self, model: Type[ModelType], db: AsyncSession):
        self.model = model
        self.db = db

    async def get(self,  obj_id: int) -> Optional[ModelType]:
        stmt = select(self.model).where(self.model.id == obj_id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_all(self) -> List[ModelType]:
        stmt = select(self.model)
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def create(self, obj_in: dict) -> ModelType:
        db_obj = self.model(**obj_in)
        self.db.add(db_obj)
        await self.db.commit()
        await self.db.refresh(db_obj)
        return db_obj

    async def update(self, obj_id: int, update_data: dict) -> ModelType:
        """Update a record by ID"""
        db_obj = await self.get(obj_id)
        if not db_obj:
            raise HTTPException(status_code=404, detail=f"{self.model.__name__} not found")
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        self.db.add(db_obj)
        await self.db.commit()
        await self.db.refresh(db_obj)
        return db_obj

    async def delete(self, obj_id: int) -> bool:
        """Delete a record by ID"""
        db_obj = await self.get(obj_id)
        if not db_obj:
            return False
        await self.db.delete(db_obj)
        await self.db.commit()
        return True














