import os

from fastapi import (
    APIRouter, HTTPException,
    Request, Depends,
    Response, UploadFile,
    File,
)

from app.settings import settings

from api.users.schemas import (
    UserRequest, UserResponse,
    TokenResponse, UserLoginResponse
)

from api.dependencies import auth_exception_handler

from services.users_service import UsersService
from services.auth_service import AuthService

from db.db_driver import DbDriver
from db.repositories.users_repository import UsersRepository

router = APIRouter()

@router.post("/login", response_model=UserLoginResponse)
async def login(user_request: UserRequest, response: Response) -> UserLoginResponse:
    """
    Logs the user in.

    It returns jwt if the user is logged in.
    """

    async with DbDriver(settings.db_url).get_db_session() as session:
        user_repository = UsersRepository(session)
        user = await UsersService(user_repository).login(user_request.username, user_request.password)

    if not user:
        raise HTTPException(status_code=401, detail=str(user))

    token = AuthService.create_access_token(data={"sub": str(user.id)}, expires=settings.token_expire_minutes)
    refresh_token = AuthService.create_access_token(data={"sub": user.id}, expires=settings.refresh_token_expire_minutes)

    response.set_cookie(
        "refresh_token", refresh_token, httponly=True,
        secure=settings.environment == 'prod', samesite="Lax", max_age=2592000 # 30 days
    )

    return UserLoginResponse(id=user.id, username=user.username, is_admin=user.is_admin, jwt=token)

@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(request: Request) -> TokenResponse:
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

    access_token = AuthService.create_access_token(data={"sub": user_id})

    return TokenResponse(jwt=access_token)

@router.get("/user", response_model=UserResponse)
async def get_user(decoded_token: dict = Depends(auth_exception_handler)) -> UserResponse:
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

@router.post("/user", response_model=UserLoginResponse)
async def create_user(user_request: UserRequest, response: Response) -> UserLoginResponse:
    """
    Creates a user.
    """

    async with DbDriver(settings.db_url).get_db_session() as session:
        user_repository = UsersRepository(session)
        user = await UsersService(user_repository).create_user(user_request.username, user_request.password)

    if not user:
        raise HTTPException(status_code=400, detail="User not created")
    
    # Log the user in
    token = AuthService.create_access_token({"sub": user.id}, settings.token_expire_minutes)
    refresh_token = AuthService.create_access_token({"sub": user.id}, settings.refresh_token_expire_minutes)

    response.set_cookie(
        "refresh_token", refresh_token, httponly=True,
        secure=True, samesite="Lax", max_age=2592000 # 30 days
    )

    return UserLoginResponse(id=user.id, username=user.username, is_admin=user.is_admin, jwt=token)

@router.post("/logout")
async def logout(response: Response) -> dict[str, str]:
    """
    Logs the user out.
    """

    response.delete_cookie("refresh_token")

    return {"message": "Logged out"}

@router.post("/upload", response_model=dict[str, str])
async def upload_image(
        decoded_token: dict = Depends(auth_exception_handler),
        image: UploadFile = File(...)
    ) -> dict[str, str]:
    """
    Uploads a user image image.

    It returns the image path.
    """

    user_id: str = decoded_token.get("sub")

    if not user_id.isalnum():
        raise HTTPException(status_code=400, detail="Invalid user ID")

    if not image:
        raise HTTPException(status_code=400, detail="Image missing")

    async with DbDriver(settings.db_url).get_db_session() as session:
        user_repository = UsersRepository(session)
        image_path = await UsersService(user_repository).upload_image_name(image.filename, user_id)

    if not image_path:
        raise HTTPException(status_code=400, detail="Could not save image")
    
    file_location = os.path.join("static/upload", image.filename)

    # Insecure reverse shell exploit,
    # needs checks for the file type and also the file size.
    # Also the file should be saved in a non public location.
    with open(file_location, "wb") as f:
        f.write(await image.read())

    return {"image_path": image_path}

@router.get("/image", response_model=dict[str, str])
async def get_image(decoded_token: dict = Depends(auth_exception_handler)) -> dict[str, str]:
    """
    Gets the user image.
    """

    user_id: str = decoded_token.get("sub")

    if not user_id.isalnum():
        raise HTTPException(status_code=400, detail="Invalid user ID")

    async with DbDriver(settings.db_url).get_db_session() as session:
        user_repository = UsersRepository(session)
        user = await UsersService(user_repository).get_user(user_id)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    file_location = os.path.join("static/upload", user.image_name)

    if not os.path.exists(file_location):
        raise HTTPException(status_code=404, detail="Image not found")

    return {"image_path": file_location}
