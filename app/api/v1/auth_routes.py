from typing import Optional, Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Cookie, Depends, HTTPException, Response, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from app.db.session import get_db
from app.schemas.auth import AuthResponse, Token, LoginRequest
from app.schemas.user import UserCreate
from app.services import auth_service as auth_service

router = APIRouter()


@router.post(
    "/signup", response_model=AuthResponse, status_code=status.HTTP_201_CREATED
)
async def signup(
        body: UserCreate,
        response: Response,
        db: Annotated[AsyncSession, Depends(get_db)]):
    """ Signup endpoint for users. """

    auth_response, refresh_token = await auth_service.signup_user(db, body)

    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=True,
        samesite="strict",
        max_age=7 * 24 * 60 * 60,
    )

    return auth_response


@router.post("/login", response_model=Token)
async def login(
        login_data: LoginRequest,
        db: AsyncSession=Depends(get_db)):
    """ Login endpoint using OAuth2 password flow """
    access_token, refresh_token = await auth_service.login_user(db, login_data.email, login_data.password)

    response = JSONResponse(
        content={
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
        max_age=7 * 24 * 60 * 60,  # 7 days
    )
    return response


@router.post("/refresh", response_model=Token, status_code=status.HTTP_200_OK)
async def refresh(
    refresh_token: Optional[str] = Cookie(None),
    db: AsyncSession = Depends(get_db)
):
    """ Refresh access token using http-only refresh token cookies """
    if not refresh_token:
        raise HTTPException(status_code=401, detail="Refresh token required")

    access_token, refresh_token = await auth_service.refresh_user_session(db, refresh_token)

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
