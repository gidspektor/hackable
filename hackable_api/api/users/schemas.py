from pydantic import BaseModel, Field

from app.settings import settings


class TokenResponse(BaseModel):
    """
    Response schema for a token.
    """

    jwt: str


class UserResponse(BaseModel):
    """
    Response schema for a user.
    """

    id: int
    username: str
    is_admin: bool


class UserRequest(BaseModel):
    """
    Request schema for creating a user.
    """

    username: str = Field(max_length=settings.request_max_length)
    password: str = Field(max_length=settings.request_max_length, min_length=settings.password_min_length)


class UserLoginResponse(BaseModel):
    """
    Response schema for a user login.
    """

    id: int
    username: str
    is_admin: bool
    jwt: str


class passwordChangeRequest(BaseModel):
    """
    Request schema for changing a password.
    """

    old_password: str = Field(max_length=settings.request_max_length, min_length=settings.password_min_length)
    new_password: str = Field(max_length=settings.request_max_length, min_length=settings.password_min_length)
    new_password_match: str = Field(max_length=settings.request_max_length, min_length=settings.password_min_length)
