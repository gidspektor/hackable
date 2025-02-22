from fastapi import APIRouter, HTTPException

from hackable_api.api.user.schemas import (
    UserRequest, UserResponse
)
from hackable_api.services.users_service import UsersService

router = APIRouter()

@router.post("/login", response_model=UserResponse)
async def login(user_request: UserRequest) -> UserResponse:
    """
    Logs the user in.

    It returns jwt if the user is logged in.
    """

    user = UsersService.login(user_request['username'], user_request['password'])

    if not user:
        raise HTTPException(status_code=401, detail=str(e))

async def refresh_token() -> str:
    """
    Refreshes the user token.

    It returns jwt if the user is logged in.
    """
    
    user = UsersService.get_user(user_id)
    user = AuthService.verify_refresh_token(refresh_token)
    access_token = AuthService.create_access_token(data={"sub": user.username})

    return access_token