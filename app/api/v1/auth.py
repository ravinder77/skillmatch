from typing import Annotated
from fastapi import APIRouter, Cookie, Depends, HTTPException, Response, status
from app.dependencies.auth import get_auth_service
from app.dependencies.user import get_user_service
from app.schemas.auth import TokenResponse, LoginRequest
from app.schemas.user import UserCreate, UserResponse
import logging
from app.services.auth_service import AuthService
from app.services.user_service import UserService

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post(
    "/signup", response_model=UserResponse, status_code=status.HTTP_201_CREATED
)
async def signup(
        body: UserCreate,
        user_service: Annotated[UserService, Depends(get_user_service)]
):
    """Sign up new user"""
    new_user = await user_service.create_user(body)
    return new_user

@router.post("/login", response_model=TokenResponse, status_code=status.HTTP_200_OK)
async def login(
        login_data: LoginRequest,
        response: Response,
        auth_service: Annotated[AuthService, Depends(get_auth_service)]
):
    """Authenticate user and issue tokens"""
    tokens = await auth_service.authenticate_user(login_data.email, login_data.password)

    response.set_cookie(
        key="refresh_token",
        value=tokens.refresh_token,
        httponly=True,
        secure=True,
        samesite="strict",
        max_age=7 * 24 * 60 * 60,  # 7 days
    )

    return TokenResponse(
        access_token=tokens.access_token,
        token_type=tokens.token_type,
    )


@router.post("/refresh", response_model=TokenResponse, status_code=status.HTTP_200_OK)
async def refresh(
    response: Response,
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
    refresh_token: str = Cookie(None),
):
    """ Refresh access token using http-only refresh token cookies """
    if not refresh_token:
        raise HTTPException(status_code=401, detail="Refresh token required")

    try:
        tokens = await auth_service.refresh_tokens(refresh_token)
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))

    response.set_cookie(
        key="refresh_token",
        value=tokens.refresh_token,
        httponly=True,
        secure=True,
        samesite="strict",
        max_age=7 * 24 * 60 * 60,
    )
    logger.info("Access token refreshed successfully")
    return TokenResponse(
        access_token=tokens.access_token,
        token_type=tokens.token_type
    )

@router.post("/logout", status_code=status.HTTP_200_OK)
async def logout(response: Response):
    """
    logout user by clearing refresh token cookies
    """
    response.delete_cookie(
        key="refresh_token",
        path="/",
        secure=True,
        httponly=True,
        samesite="strict",
    )
    return {"message": "Logout successful"}
