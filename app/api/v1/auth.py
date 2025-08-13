from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import timedelta
from app.core.security import hash_password, verify_password, create_access_token, decode_token

from app.core.config import settings
from app.core.exceptions import SkillMatchException

router = APIRouter(prefix="/auth", tags=["auth"])


# OAUTH2 Password Flow

