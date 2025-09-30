from fastapi import HTTPException
from jose import JWTError

from app.core.security import (
    hash_password, create_access_token, create_refresh_token, verify_password, decode_token)
from app.schemas.auth import AuthResponse
from app.schemas.user import UserCreate
from sqlalchemy.orm import Session
from app.models.user import User
from app.core.enums import UserRole
from app.repositories import auth as auth_repository


def signup_user(db: Session, body: UserCreate) -> tuple[AuthResponse, str]:
    if auth_repository.get_user_by_username(db, body.username):
        raise HTTPException(status_code=400, detail="Username already exists")
    if auth_repository.get_user_by_email(db, str(body.email)):
        raise HTTPException(status_code=400, detail="Email already exists")

    # build sqlalchemy model
    new_user = User(
        username=body.username,
        first_name=body.first_name,
        last_name=body.last_name,
        email=str(body.email),
        hashed_password=hash_password(body.password),
        role=body.role or UserRole.CANDIDATE,
        is_active=True,
    )


    auth_repository.create_user(db, new_user)
    access_token, refresh_token = generate_tokens(new_user)

    auth_body =  AuthResponse(
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
    user = auth_repository.get_user_by_email(db, email)
    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect email or password")

    access_token, refresh_token = generate_tokens(user)
    return access_token, refresh_token


def refresh_user_session(db: Session, refresh_token: str) -> tuple[str, str]:
    try:
        payload = decode_token(refresh_token)
        user_id = payload.get("id")
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid refresh token")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    user = auth_repository.get_user_by_id(db, user_id)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    access_token, new_refresh_token = generate_tokens(user)

    return access_token, new_refresh_token


def generate_tokens(user: User) -> tuple[ str, str]:
    access_token = create_access_token({
        "id": user.id,
        "email": user.email,
        "role": user.role.value,
    })
    refresh_token = create_refresh_token({
        "id": user.id,
        "email": user.email,
        "role": user.role.value,
    })
    return access_token, refresh_token




