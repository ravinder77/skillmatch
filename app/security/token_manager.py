from datetime import datetime, timedelta
from typing import Any, Dict

from jose import ExpiredSignatureError, jwt

from app.config.settings import settings


class TokenManager:
    """Manages JWT token generation and validation."""

    def __init__(
        self,
        refresh_secret_key: str = settings.REFRESH_TOKEN_SECRET,
        access_secret_key: str = settings.ACCESS_TOKEN_SECRET,
        algorithm: str = settings.ALGORITHM,
    ):
        self.refresh_secret_key = refresh_secret_key
        self.access_secret_key = access_secret_key
        self.algorithm = algorithm

    def create_access_token(self, data: Dict[str, Any]) -> str:
        """Generate a short-lived access token."""
        payload = data.copy()
        now = datetime.now()
        expire = now + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRY)
        payload.update({"exp": expire, "iat": now})
        return jwt.encode(payload, self.access_secret_key, algorithm=self.algorithm)

    def create_refresh_token(self, data: Dict[str, Any]) -> str:
        """Generate a longer-lived refresh token."""
        payload = data.copy()
        now = datetime.now()
        expire = now + timedelta(minutes=settings.REFRESH_TOKEN_EXPIRY)
        payload.update({"exp": expire, "iat": now})
        return jwt.encode(payload, self.refresh_secret_key, algorithm=self.algorithm)

    def decode_token(self, token: str, is_refresh: bool = False) -> Dict[str, Any]:
        """Decode a JWT token and return its payload."""
        secret_key = self.refresh_secret_key if is_refresh else self.access_secret_key
        try:
            payload = jwt.decode(token, secret_key, algorithms=[self.algorithm])
            return payload
        except ExpiredSignatureError:
            raise ValueError("Token has expired")

    def verify_token(self, token: str, is_refresh: bool = False) -> bool:
        """Verify if a token is valid and not expired."""
        try:
            self.decode_token(token, is_refresh)
            return True
        except ValueError:
            return False
