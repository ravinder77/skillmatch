from datetime import datetime, timedelta
from typing import Optional
from fastapi import HTTPException
from jose import JWTError, jwt
from passlib.hash import bcrypt
from app.core.config import settings


# Password Utilities
def hash_password(password: str) -> str:
    """
    Hash a password.
    :param password: takes a plain text password and hashes it
    :return: returns the hashed password string
    """
    return bcrypt.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a hashed password against the plain text.
    :param plain_password: takes a plain text password
    :param hashed_password: takes a hashed text password
    :return: verify the hashed password against the plain text and return True or False
    """
    return bcrypt.verify(plain_password, hashed_password)


# TOKENS UTILITIES
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Generate an access token using a JWT token.
    """
    to_encode = data.copy()
    expire = datetime.now() + (
        expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({"exp": expire})
    token = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return token


# Create Refresh Token
def create_refresh_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Generate an refresh token using a JWT token.
    """
    to_encode = data.copy()
    expire = datetime.now() + (
        expires_delta or timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    )
    to_encode.update({"exp": expire})
    token = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return token


def decode_token(token: str) -> Optional[dict]:
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        return payload

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
