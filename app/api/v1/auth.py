from datetime import datetime, timedelta
from typing import Optional, Annotated
from fastapi import APIRouter, Cookie, Depends, HTTPException, Response, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.core.enums import UserRole
from app.core.security import (
    create_access_token,
    create_refresh_token,
    decode_token,
    hash_password,
    verify_password,
)
from app.db.session import get_db
from app.models.user import User
from app.schemas.auth import AuthResponse, Token, TokenData
from app.schemas.user import UserCreate

router = APIRouter()

# OAUTH2 Password Flow
oauth2_scheme = OAuth2PasswordBearer("auth/login")


@router.post(
    "/signup", response_model=AuthResponse, status_code=status.HTTP_201_CREATED
)
async def signup(
        body: UserCreate,
        db: Annotated[Session, Depends(get_db)]):
    """ Signup endpoint for users. """

    # check if username exists
    if db.query(User).filter(User.username == body.username).first():
        raise HTTPException(status_code=400, detail="Username already exists")

    # check if email is already registered
    if db.query(User).filter(User.email == body.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")

    # hash password before saving to db
    hashed_pw = hash_password(body.password)

    new_user: User = User(
        username=body.username,
        first_name=body.first_name,
        last_name=body.last_name,
        email=str(body.email),
        hashed_password=hashed_pw,
        role= body.role or UserRole.CANDIDATE,
        is_active=True,
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Generate JWT token
    access_token = create_access_token(
        {"id": new_user.id, "email": new_user.email, "role": new_user.role.value}
    )

    refresh_token = create_refresh_token(
        {"id": new_user.id, "email": new_user.email, "role": new_user.role.value}
    )

    response = JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={
            "id": new_user.id,
            "username": new_user.username,
            "email": new_user.email,
            "first_name": new_user.first_name,
            "last_name": new_user.last_name,
            "role": new_user.role.value,
            "access_token": access_token,
            "token_type": "bearer",
        }
    )

    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=True,
        samesite="strict",
        max_age=7 * 24 * 60 * 60,
    )

    return response


@router.post("/login", response_model=Token, status_code=status.HTTP_200_OK)
async def login(form_data: OAuth2PasswordRequestForm = Depends(),
        db: Session= Depends(get_db)):
    """ Login endpoint using OAuth2 password flow """
    # check if user exists
    user: Optional[User] = (
        db.query(User).filter(User.email == form_data.username).first()
    )

    if not user:
        raise HTTPException(status_code=401, detail="Incorrect username or password")

    if not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect username or password")

    # create JWT access-token
    access_token = create_access_token(
        {
            "id": user.id,
            "email": user.email,
            "role": user.role.value,
        }
    )
    refresh_token = create_refresh_token(
        {
            "id": user.id,
            "email": user.email,
            "role": user.role.value,
        }
    )

    response = JSONResponse(
        content={"access_token": access_token, "token_type": "bearer"}
    )

    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=True,
        samesite="strict",
        max_age=7 * 24 * 60 * 60,  # 7 days
    )

    return response


@router.post("/refresh", response_model=Token, status_code=status.HTTP_200_OK)
async def refresh(
    refresh_token: Optional[str] = Cookie(None),
        db: Session = Depends(get_db)
):
    """ Refresh access token using http-only refresh token cookies """
    if not refresh_token:
        raise HTTPException(status_code=401, detail="Refresh token required")
    try:
        payload = decode_token(refresh_token)
        user_id = payload.get("id")
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid refresh token")
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    # create new access token
    access_token = create_access_token(
        {
            "id": user.id,
            "email": user.email,
            "role": user.role.value,
        }
    )
    # also create new refresh token for rotation
    refresh_token = create_refresh_token(
        {
            "id": user.id,
            "email": user.email,
            "role": user.role.value,
        }
    )

    response = JSONResponse(
        content={"access_token": access_token, "token_type": "bearer"}
    )
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=True,
        samesite="strict",
        max_age=7 * 24 * 60 * 60,
    )
    return response


@router.post("/logout", status_code=status.HTTP_200_OK)
async def logout(response: Response):
    """
    logout user by clearing refresh token cookies
    """
    response.delete_cookie(
        key="refresh_token",
        path="/",  # use same path which was used to set the cookie
        secure=True,
        # domain="None", # optional: set domain if cookie was set with domain
        httponly=True,
        samesite="strict",
    )
    return {"message": "Logout successful"}
