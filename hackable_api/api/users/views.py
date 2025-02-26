from fastapi import APIRouter, HTTPException, Request

from api.users.schemas import (
    UserRequest, UserResponse
)
from services.users_service import UsersService
from services.auth_service import AuthService

router = APIRouter()

@router.post("/login", response_model=UserResponse)
async def login(user_request: UserRequest) -> UserResponse:
    """
    Logs the user in.

    It returns jwt if the user is logged in.
    """

    user = UsersService.login(user_request.username, user_request.password)

    if not user:
        raise HTTPException(status_code=401, detail=str(user))

    access_token = AuthService.create_access_token(data={"sub": user.id})

    return UserResponse(id=user.id, username=user.username, is_admin=user.is_admin, jwt=access_token)

@router.post("/refresh", response_model=UserResponse)
async def refresh_token(request: Request) -> UserResponse:
    """
    Refreshes the user token.

    It returns jwt if the user is logged in.
    """

    refresh_token = request.cookies.get("refresh_token")

    if not refresh_token:
        raise HTTPException(status_code=401, detail="Refresh token missing")

    decoded_token = AuthService.verify_token(refresh_token)

    if not decoded_token:
        raise HTTPException(status_code=401, detail="Refresh token invalid")

    user_id: str = decoded_token.get("sub")
    user = UsersService.get_user(user_id)

    if not user:
        raise HTTPException(status_code=401, detail=str(user))

    access_token = AuthService.create_access_token(data={"sub": user.id})

    return UserResponse(id=user.id, username=user.username, is_admin=user.is_admin, jwt=access_token)
