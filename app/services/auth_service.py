from fastapi import HTTPException
from jose import JWTError, jwt
from sqlalchemy import select
from starlette import status
from app.core.config import settings
from app.core.security import (
    hash_password, create_access_token, create_refresh_token, verify_password, decode_token
)
from app.schemas.auth import AuthResponse
from app.schemas.user import UserCreate
from sqlalchemy.orm import Session
from app.models.user import User
from app.core.enums import UserRole
from app.repositories import user_repository


def signup_user(db: Session, body: UserCreate) -> tuple[AuthResponse, str]:
    if user_repository.get_by_username(db, body.username):
        raise HTTPException(status_code=400, detail="Username already exists")
    if user_repository.get_by_email(db, str(body.email)):
        raise HTTPException(status_code=400, detail="Email already exists")

    # build sqlalchemy model
    new_user = User(
        username=body.username,
        first_name=body.first_name,
        last_name=body.last_name,
        email=str(body.email),
        hashed_password=hash_password(body.password),
        role=UserRole.CANDIDATE,
        is_active=True,
    )

    user_repository.create_user(db, new_user)
    access_token, refresh_token = generate_tokens(new_user)

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


def login_user(db: Session, email: str, password: str) -> tuple[str, str]:
    user = user_repository.get_by_email(db, email)
    if not user or not verify_password(password, str(user.hashed_password)):
        raise HTTPException(status_code=400, detail="Incorrect email or password")

    access_token, refresh_token = generate_tokens(user)
    return access_token, refresh_token


def refresh_user_session(db: Session, refresh_token: str) -> tuple[str, str]:
    try:
        payload = decode_token(refresh_token)
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid refresh token")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    user = user_repository.get_by_id(db, user_id)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    access_token, new_refresh_token = generate_tokens(user)

    return access_token, new_refresh_token


def generate_tokens(user: User) -> tuple[str, str]:
    access_token = create_access_token({
        "sub": user.id,
        "email": user.email,
        "role": user.role.value,
    })
    refresh_token = create_refresh_token({
        "sub": user.id,
        "email": user.email,
        "role": user.role.value,
    })
    return access_token, refresh_token


def get_user_from_token(db: Session, token: str) -> User:
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

    # Fetch user from DB
    user = db.execute(select(User).where(User.id == user_id)).scalar_one_or_none()
    if user is None:
        raise credentials_exception

    return user
