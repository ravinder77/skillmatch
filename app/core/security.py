from datetime import timedelta, datetime
from typing import Optional
from jose import jwt, JWTError
from passlib.context import CryptContext
from app.core.config import settings
from app.core.exceptions import SkillMatchException



#Password Hashing Context
context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# Password Utilities

def hash_password(password: str) -> str:
    """
    Hash a password.
    :param password: takes a plain text password and hashes it
    :return: returns the hashed password string
    """
    return context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a hashed password against the plain text.
    :param plain_password: takes a plain text password
    :param hashed_password: takes a hashed text password
    :return:
    """
    return context.verify(plain_password, hashed_password)


# TOKENS UTILITIES

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Generate an access token using a JWT token.
    """
    to_encode = data.copy()
    expire = datetime.now() + (expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    token = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return token


def decode_token(token: str) -> Optional[dict]:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except JWTError:
        raise SkillMatchException("Invalid or expired token", status_code=401)

