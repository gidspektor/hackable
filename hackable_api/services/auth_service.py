from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta

from hackable_api.app.settings import settings


class AuthService:
    def create_access_token(data: dict, expires_delta: timedelta | None = None):
        to_encode = data.copy()
        expire = datetime.utcnow() + (expires_delta or timedelta(minutes=settings.access_token_expire_minutes))
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)


    def verify_refresh_token(refresh_token: str):
        try:
            payload = jwt.decode(refresh_token, REFRESH_SECRET_KEY, algorithms=[ALGORITHM])
            username: str = payload.get("sub")
            if not username:
                raise HTTPException(status_code=401, detail="Invalid refresh token")

            user = db.query(User).filter(User.username == username).first()
            if not user:
                raise HTTPException(status_code=401, detail="User not found")

            return user
        except JWTError:
            raise HTTPException(status_code=401, detail="Invalid refresh token")