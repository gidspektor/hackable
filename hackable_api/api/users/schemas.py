from pydantic import BaseModel, Field

from app.settings import settings


class UserResponse(BaseModel):
    """
    Response schema for a user.
    """

    id: int
    username: str
    is_admin: bool
    jwt: str


class UserRequest(BaseModel):
    """
    Request schema for creating a user.
    """

    username: str = Field(max_length=settings.request_max_length)
    password: str = Field(max_length=settings.request_max_length)
