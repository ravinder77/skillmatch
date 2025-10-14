from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from jose import JWTError, jwt
from starlette import status
from app.core.config import settings
from app.core.security import (
    hash_password, create_access_token, create_refresh_token, verify_password, decode_token
)
from app.schemas.auth import AuthResponse
from app.schemas.user import UserCreate
from app.models.user import User
from app.core.enums import UserRole
from app.repositories import user_repository


async def signup_user(db: AsyncSession, body: UserCreate) -> tuple[AuthResponse, str]:
    # --validate uniqueness
    if await user_repository.get_by_username(db, body.username):
        raise HTTPException(status_code=400, detail="Username already exists")

    if await user_repository.get_by_email(db, str(body.email)):
        raise HTTPException(status_code=400, detail="Email already exists")

    # build user model
    new_user = User(
        username=body.username,
        first_name=body.first_name,
        last_name=body.last_name,
        email=str(body.email),
        hashed_password=hash_password(body.password),
        role=UserRole.CANDIDATE,
        is_active=True,
    )

    # save user
    await user_repository.create_user(db, new_user)
    # generate tokens
    access_token, refresh_token = generate_tokens(new_user)

    # build response
    auth_body = AuthResponse(
        id=new_user.id,
        email=new_user.email,
        username=new_user.username,
        first_name=new_user.first_name,
        last_name=new_user.last_name,
        role=new_user.role,
        access_token=access_token,
    )

    return auth_body, refresh_token


async def login_user(db: AsyncSession, email: str, password: str) -> tuple[str, str]:
    """
      Returns access_token and refresh_token for a user
      """
    user: User = await user_repository.get_by_email(db, email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Credentials"
        )
    if not verify_password(password, str(user.hashed_password)):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Credentials"
        )

    access_token, refresh_token = generate_tokens(user.id, user.email, user.role)
    return access_token, refresh_token


async def refresh_tokens(db: AsyncSession, refresh_token: str) -> tuple[str, str]:
    try:
        payload = decode_token(refresh_token)
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid refresh token")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    user: User = await user_repository.get_by_id(db, user_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )

    access_token, new_refresh_token = generate_tokens(user.id, user.email, user.role)

    return access_token, new_refresh_token

def generate_tokens(user_id: int, email: str, role: UserRole) -> tuple[str, str]:
    """
    Generates a new access token and refresh token
    """
    access_token = create_access_token({
        "sub": user_id,
        "email": email,
        "role": role.value,
    })
    refresh_token = create_refresh_token({
        "sub": id,
        "email": email,
        "role": role.value,
    })
    return access_token, refresh_token


async def get_user_from_token(db: AsyncSession, token: str) -> User:

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials.",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=settings.ALGORITHM)
        user_id: int = payload.get("sub")  # 'sub' stands for subject (user id)
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    # Fetch user
    user = await user_repository.get_by_id(db, user_id)
    if user is None:
        raise credentials_exception

    return user
