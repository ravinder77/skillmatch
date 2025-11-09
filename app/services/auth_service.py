from fastapi import HTTPException
from starlette import status
from app.repositories.user_repository import UserRepository
from app.schemas.auth import Tokens
from app.security.password_hasher import PasswordHasher
from app.security.token_manager import TokenManager


class AuthService:
    def __init__(self, repo: UserRepository):
        self.user_repo = repo
        self.password_hasher = PasswordHasher()
        self.token_manager = TokenManager()

    async def authenticate_user(self, email: str, password: str) -> Tokens:
        """
          Returns access_token and refresh_token for a user
          """
        user = await self.user_repo.get_by_email(email)

        if not user or not self.password_hasher.verify(password, str(user.password_hash)):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid Credentials"
            )

        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User account is not active"
            )

        payload = {
            "sub": str(user.id),
            "role": user.role,
        }

        access_token = self.token_manager.create_access_token(payload)
        refresh_token = self.token_manager.create_refresh_token(payload)


        return Tokens(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer",
        )

    async def refresh_tokens(self, refresh_token: str) -> Tokens:
        """Generate new token pair using refresh token"""

        payload = self.token_manager.decode_token(refresh_token)
        user_id = int(payload["sub"])
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid refresh token")

        user = await self.user_repo.get_by_id(user_id)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found"
            )
        new_payload = {
            "sub": str(user.id),
            "role": user.role,
        }

        access_token = self.token_manager.create_access_token(new_payload)
        new_refresh_token = self.token_manager.create_refresh_token(new_payload)

        return Tokens(
            access_token=access_token,
            refresh_token=new_refresh_token,
            token_type="bearer",
        )