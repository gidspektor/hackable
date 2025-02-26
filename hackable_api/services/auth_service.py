from jose import jwt
from jose.exceptions import JWTError
from datetime import datetime, timedelta

from app.settings import settings


class AuthService:
    def create_access_token(data: dict):
        to_encode = data.copy()
        expire = datetime.utcnow() + (timedelta(minutes=settings.access_token_expire_minutes))
        to_encode.update({"exp": expire})

        return jwt.encode(to_encode, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)

    def verify_token(token: str):
        try:
            payload = jwt.decode(token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])
            return payload
        except JWTError:
            return None
