from fastapi import (
    APIRouter, HTTPException,
    Request, Depends,
    Response,
)

from app.settings import settings

from api.users.schemas import (
    UserRequest, UserResponse
)

from api.dependencies import auth_exception_handler

from services.users_service import UsersService
from services.auth_service import AuthService

from db.db_driver import DbDriver
from db.repositories.users_repository import UsersRepository

router = APIRouter()

@router.post("/login", response_model=UserResponse)
async def login(user_request: UserRequest, response: Response) -> UserResponse:
    """
    Logs the user in.

    It returns jwt if the user is logged in.
    """

    async with DbDriver(settings.db_url).get_db_session() as session:
        user_repository = UsersRepository(session)
        user = await UsersService(user_repository).login(user_request.username, user_request.password)

    if not user:
        raise HTTPException(status_code=401, detail=str(user))

    token = AuthService.create_access_token({"sub": user.id}, settings.token_expire_minutes)
    refresh_token = AuthService.create_access_token({"sub": user.id}, settings.refresh_token_expire_minutes)

    response.set_cookie(
        "refresh_token", refresh_token, httponly=True,
        secure=True, samesite="Lax", max_age=2592000 # 30 days
    )

    return UserResponse(id=user.id, username=user.username, is_admin=user.is_admin, jwt=token)

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

    if not user_id.isalnum():
        raise HTTPException(status_code=400, detail="Invalid user ID")

    async with DbDriver(settings.db_url).get_db_session() as session:
        user_repository = UsersRepository(session)
        user = await UsersService(user_repository).get_user(user_id)

    if not user:
        raise HTTPException(status_code=401, detail=str(user))

    access_token = AuthService.create_access_token(data={"sub": user.id})

    return UserResponse(id=user.id, username=user.username, is_admin=user.is_admin, jwt=access_token)

@router.get("/user", response_model=UserResponse)
async def get_user(decoded_token: str = Depends(auth_exception_handler)) -> UserResponse:
    """
    Gets the user.
    """

    user_id: str = decoded_token.get("sub")

    if not user_id.isalnum():
        raise HTTPException(status_code=400, detail="Invalid user ID")

    async with DbDriver(settings.db_url).get_db_session() as session:
        user_repository = UsersRepository(session)
        user = await UsersService(user_repository).get_user(user_id)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return UserResponse(id=user.id, username=user.username, is_admin=user.is_admin)

@router.post("/upload", dependencies=[Depends(auth_exception_handler)])
async def upload_image(request: Request) -> dict[str, str]:
    """
    Uploads a user image image.

    It returns the image path.
    """

    image = request.get("image")

    if not image:
        raise HTTPException(status_code=400, detail="Image missing")
    
    async with DbDriver(settings.db_url).get_db_session() as session:
        user_repository = UsersRepository(session)
        image_path = await UsersService(user_repository).upload_image(image)

    return {"image_path": image_path}
