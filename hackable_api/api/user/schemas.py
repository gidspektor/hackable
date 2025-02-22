from pydantic import BaseModel

from hackable_api.app.settings import settings


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

    username: str
    password: str

    class Config:
        str_max_length = settings.request_max_lenth
        min_length = settings.password_min_length
