from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, HTTPException
from starlette import status
from fastapi.security import OAuth2PasswordBearer
from app.db.session import get_db
from app.models.user import User
from app.core.enums import UserRole
from app.services import auth_service

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

async def get_current_user(
        token: Annotated[str, Depends(oauth2_scheme)],
        db: Annotated[AsyncSession, Depends(get_db)]) -> User:
    """
    Dependency that extracts the current user from the JWT token.
    Raises 401 if the token is invalid or the user is not authenticated
    """
    user = await auth_service.get_user_from_token(db, token)
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