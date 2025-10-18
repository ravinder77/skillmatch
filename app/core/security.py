from datetime import datetime, timedelta
from typing import Optional
from fastapi import HTTPException
from jose import JWTError, jwt, ExpiredSignatureError
from passlib.hash import argon2
from app.core.config import settings
from app.core.enums import UserRole


# Password Utilities
def hash_password(password: str) -> str:
    """
    Hash a password.
    :param password: takes a plain text password and hashes it
    :return: returns the hashed password string
    """
    return argon2.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a hashed password against the plain text.
    :param plain_password: takes a plain text password
    :param hashed_password: takes a hashed text password
    :return: verify the hashed password against the plain text and return True or False
    """
    return argon2.verify(plain_password, hashed_password)


# TOKENS UTILITIES
def create_access_token(data: dict) -> str:
    """
    Generate an access token using a JWT token.
    """
    to_encode = data.copy()
    now = datetime.now()
    expire = now + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRY)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


# Create Refresh Token
def create_refresh_token(data: dict) -> str:
    """
    Generate an refresh token using a JWT token.
    """
    to_encode = data.copy()
    now = datetime.now()
    expire = now + timedelta (minutes=settings.REFRESH_TOKEN_EXPIRY)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def generate_tokens(user_id: int, role: UserRole) -> tuple[str, str]:
    """
    Generates a new access token and refresh token
    """
    payload = {
        "sub": str(user_id),
        "role": role.value,
        "iat": datetime.now(),
    }
    access_token = create_access_token(payload)
    refresh_token = create_refresh_token(payload)

    return access_token, refresh_token


def decode_token(token: str) -> Optional[dict]:
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        return payload
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Expired token")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

