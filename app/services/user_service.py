from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate, UserResponse, UserUpdate
from app.models import User
from app.security.password_hasher import PasswordHasher


class UserService:
    def __init__(self, db: AsyncSession):
        self.repo = UserRepository(db)
        self.password_hasher = PasswordHasher()


    async def create_user(self, user_data: UserCreate) -> UserResponse:

        # hash password
        hashed_pw = self.password_hasher.hash(user_data.password)

        # build orm model
        user = User(
            first_name=user_data.first_name,
            last_name=user_data.last_name,
            email=str(user_data.email),
            password_hash= hashed_pw,
            role=user_data.role,
        )

        # persist to repository
        new_user = await self.repo.create_user(user)
        return UserResponse.model_validate(new_user)

    async def get_user_by_email(self, email: str) -> UserResponse:

        existing_user = self.repo.get_by_email(email)
        if not existing_user:
            raise HTTPException(status_code=404, detail="User not found")

        return UserResponse.model_validate(existing_user)

    async def get_user_by_id(self, user_id: int) -> UserResponse:
        existing_user = self.repo.get_by_id(user_id)
        if not existing_user:
            raise HTTPException(status_code=404, detail="User not found")
        return UserResponse.model_validate(existing_user)


    async def update_user(self, user_id: int, user_data: UserUpdate) -> UserResponse:

        # convert to dict and pass only those fields that were provided
        data = user_data.model_dump(exclude_unset=True)

        updated_user = await self.repo.update(user_id, data)
        return UserResponse.model_validate(updated_user)




