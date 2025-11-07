from sqlalchemy import select, delete
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User
from app.repositories.base import BaseRepository


class UserRepository(BaseRepository[User]):
    def __init__(self, db: AsyncSession):
        super().__init__(User, db)
        self.db = db

    async def create_user(self, user: User) -> User:
        try:
            self.db.add(user)
            await self.db.commit()
            await self.db.refresh(user)
            return user
        except IntegrityError:
            await self.db.rollback()
            raise HTTPException(status_code=400, detail="User not found")
        except Exception:
            await self.db.rollback()
            raise HTTPException(status_code=500, detail="Internal Server Error")

    async def get_by_id(self, user_id: int) -> User | None:
        stmt = select(User).where(User.id == user_id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_email(self, email: str) -> User | None:
        stmt = select(User).where(User.email == email)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def delete(self, user_id: int) -> None:
        stmt = delete(User).where(User.id == user_id)
        await self.db.execute(stmt)
        await self.db.commit()


    async def update(self, user_id: int, user_data: dict) -> User:

        db_user = await self.get_by_id(user_id)
        if not db_user:
            raise HTTPException(status_code=404, detail="User not found")

        for key, value in user_data.items():
            setattr(db_user, key, value)

        await self.db.commit()
        await self.db.refresh(db_user)
        return db_user












