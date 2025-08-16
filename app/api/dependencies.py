from typing import Any

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from sqlalchemy.orm import Session
from starlette import status

from app.db.session import get_db
from app.models.user import User
from app.core.security import decode_token


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")



def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = decode_token(token)
        user_id = payload.get("id")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = db.query(User).filter(User.id == user_id).first()

    if user is None:
        raise credentials_exception
    return user
