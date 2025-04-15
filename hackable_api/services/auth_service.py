from jose import jwt
from jose.exceptions import JWTError
from datetime import datetime, timedelta

from hackable_api.app.settings import settings


class AuthService:
    @staticmethod
    def create_access_token(data: dict, expires: int) -> jwt:
        to_encode = data.copy()
        expire = datetime.utcnow() + (timedelta(minutes=expires))
        to_encode.update({"exp": expire})

        return jwt.encode(to_encode, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)

    @staticmethod
    def verify_token(token: str) -> dict|None:
        try:
            payload = jwt.decode(token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])
            return payload
        except JWTError as e:
            print(e)
            return None
