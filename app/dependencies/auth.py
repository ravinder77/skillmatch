from typing import Annotated
from fastapi import Depends, HTTPException
from starlette import status
from fastapi.security import OAuth2PasswordBearer
from app.dependencies.user import get_user_service, get_user_repository
from app.models.user import User
from app.core.enums import UserRole
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserResponse
from app.security.token_manager import TokenManager
from app.services.auth_service import AuthService
from app.services.user_service import UserService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

async def get_current_user(
        token: Annotated[str, Depends(oauth2_scheme)],
        user_service: Annotated[UserService, Depends(get_user_service)],
) -> UserResponse:
    """
    Dependency that extracts the current user from the JWT token.
    Raises 401 if the token is invalid or the user is not authenticated
    """
    token_manager = TokenManager()
    payload = token_manager.decode_token(token)
    user_id = int(payload.get("sub"))
    user = await user_service.get_user_by_id(user_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )
    return user



async def get_current_employer(
    current_user: Annotated[User, Depends(get_current_user)]
) -> User:
    """Ensure the current user is an employer."""
    if current_user.role != UserRole.EMPLOYER:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You do not have permission to perform this action.",
        )
    return current_user


async def get_auth_service(repo: Annotated[UserRepository, Depends(get_user_repository)]) -> AuthService:
    return AuthService(repo)