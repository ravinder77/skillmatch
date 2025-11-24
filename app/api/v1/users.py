from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.db.session import get_db
from app.dependencies.auth import get_current_user
from app.models import User
from app.schemas.user import UserResponse, UserUpdate

router = APIRouter()


@router.get("/me", response_model=UserResponse)
async def read_me(current_user: Annotated[User, Depends(get_current_user)]):
    """
    Returns the current authenticated user
    """
    return {
        "id": current_user.id,
        "email": current_user.email,
        "role": current_user.role,
    }


@router.put("/me", response_model=UserResponse, status_code=status.HTTP_200_OK)
async def update_me(
    update_data: UserUpdate,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    """Update the logged-in user and returns the updated record."""

    if update_data.first_name is not None:
        current_user.first_name = update_data.first_name
    if update_data.last_name is not None:
        current_user.last_name = update_data.last_name

    # commit changes to the database

    return current_user


@router.delete("/me", status_code=status.HTTP_204_NO_CONTENT)
async def delete_me(
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> None:
    """Delete the currently authenticated user. Returns 204 NO CONTENT on success."""

    return None


@router.post("/reset-password", status_code=status.HTTP_200_OK)
async def reset_password(
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    """Reset password for the currently authenticated user."""
    pass
