import os
import shutil
import uuid

from fastapi import (
    APIRouter,
    HTTPException,
    Request,
    Depends,
    Response,
    UploadFile,
    File,
)

from app.app.settings import settings

from app.api.users.schemas import (
    UserRequest,
    UserResponse,
    TokenResponse,
    UserLoginResponse,
    passwordChangeRequest,
)

from app.api.dependencies import auth_exception_handler

from app.services.users_service import UsersService
from app.services.auth_service import AuthService

from app.db.db_driver import DbDriver
from app.db.repositories.users_repository import UsersRepository

router = APIRouter()


@router.post("/login/", response_model=UserLoginResponse)
async def login(user_request: UserRequest, response: Response) -> UserLoginResponse:
    """
    Logs the user in.

    It returns jwt if the user is logged in.
    """

    async with DbDriver(settings.db_url).get_db_session() as session:
        user_repository = UsersRepository(session)
        user = await UsersService(user_repository).login(
            user_request.username, user_request.password
        )

    if not user:
        raise HTTPException(status_code=401, detail=str(user))

    token = AuthService.create_access_token(
        data={"sub": str(user.id)}, expires=settings.token_expire_minutes
    )
    refresh_token = AuthService.create_access_token(
        data={"sub": str(user.id)}, expires=settings.refresh_token_expire_minutes
    )

    # samesite="strict"
    response.set_cookie(
        "refresh_token",
        refresh_token,
        httponly=True,
        secure=settings.environment == "prod",
        samesite="Lax",
        max_age=2592000,  # 30 days
    )

    return UserLoginResponse(
        id=user.id, username=user.username, is_admin=user.is_admin, jwt=token
    )


@router.post("/refresh/", response_model=TokenResponse)
async def refresh_token(request: Request) -> TokenResponse:
    """
    Refreshes the user token.

    It returns jwt if the user is logged in.
    """

    refresh_token = request.cookies.get("refresh_token")

    if not refresh_token:
        raise HTTPException(status_code=400, detail="Refresh token missing")

    decoded_token = AuthService.verify_token(refresh_token)

    if not decoded_token:
        raise HTTPException(status_code=401, detail="Refresh token invalid")

    user_id: str = decoded_token.get("sub")

    access_token = AuthService.create_access_token(
        data={"sub": user_id}, expires=settings.token_expire_minutes
    )

    return TokenResponse(jwt=access_token)


@router.get("/user/", response_model=UserResponse)
async def get_user(
    decoded_token: dict = Depends(auth_exception_handler),
) -> UserResponse:
    """
    Gets the user.
    """

    user_id: str = decoded_token.get("sub")

    if not user_id.isalnum():
        raise HTTPException(status_code=400, detail="Invalid user ID")

    async with DbDriver(settings.db_url).get_db_session() as session:
        user_repository = UsersRepository(session)
        user = await UsersService(user_repository).get_user(int(user_id))

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return UserResponse(id=user.id, username=user.username, is_admin=user.is_admin)


@router.post("/user/", response_model=UserLoginResponse)
async def create_user(
    user_request: UserRequest, response: Response
) -> UserLoginResponse:
    """
    Creates a user.
    """

    async with DbDriver(settings.db_url).get_db_session() as session:
        user_repository = UsersRepository(session)

        try:
            user = await UsersService(user_repository).create_user(user_request.dict())
        except ValueError as e:
            raise HTTPException(status_code=409, detail=str("Try another username")) from e

    if not user:
        raise HTTPException(status_code=400, detail="User not created")

    # Log the user in
    token = AuthService.create_access_token(
        {"sub": str(user.id)}, settings.token_expire_minutes
    )
    refresh_token = AuthService.create_access_token(
        {"sub": str(user.id)}, settings.refresh_token_expire_minutes
    )

    # samesite="strict"
    response.set_cookie(
        "refresh_token",
        refresh_token,
        httponly=True,
        secure=True,
        samesite="Lax",
        max_age=2592000,  # 30 days
    )

    return UserLoginResponse(
        id=user.id, username=user.username, is_admin=user.is_admin, jwt=token
    )


@router.post("/logout/")
async def logout(response: Response) -> dict[str, str]:
    """
    Logs the user out.
    """

    response.delete_cookie("refresh_token")

    return response


@router.patch("/upload/image/", response_model=dict)
async def upload_image(
    decoded_token: dict = Depends(auth_exception_handler), image: UploadFile = File(...)
) -> dict:
    """
    Uploads a user image image.

    It returns the image path.
    """

    user_id: str = decoded_token.get("sub")

    if not user_id.isalnum():
        raise HTTPException(status_code=400, detail="Invalid user ID")

    if not image:
        raise HTTPException(status_code=400, detail="Image missing")

    image_name = str(uuid.uuid4())

    async with DbDriver(settings.db_url).get_db_session() as session:
        user_repository = UsersRepository(session)
        image_path = await UsersService(user_repository).upload_image_name(
            image_name, int(user_id)
        )

    if not image_path:
        raise HTTPException(status_code=400, detail="Could not save image")

    # 🚨 Insecure file handling
    # Insecure reverse shell exploit,
    # needs checks for the file type.
    # Also the file should be saved in a non public location.
    file_location = os.path.join(f"{settings.app_root}/static/upload/{user_id}/", image_name)
    directory = os.path.dirname(f"{settings.app_root}/static/upload/{user_id}/")

    if os.path.exists(directory):
        shutil.rmtree(directory)

    os.makedirs(directory)

    return {"image_path": file_location.replace("/hackable_api/app/", "", 1)}


@router.get("/user/image/", response_model=dict)
async def get_image(decoded_token: dict = Depends(auth_exception_handler)) -> dict:
    """
    Gets the user image.
    """

    user_id: str = decoded_token.get("sub")

    if not user_id.isalnum():
        raise HTTPException(status_code=400, detail="Invalid user ID")

    async with DbDriver(settings.db_url).get_db_session() as session:
        user_repository = UsersRepository(session)
        image_url = await UsersService(user_repository).get_user_image_url(int(user_id))

    file_location = os.path.join(f"{settings.app_root}/static/upload/{user_id}/", image_url)

    if not os.path.exists(file_location):
        raise HTTPException(status_code=404, detail="Image not found")

    return {"image_path": file_location.replace("/hackable_api/app/", "", 1)}


@router.patch("/user/password/", response_model=dict)
async def change_password(
    password_change_request: passwordChangeRequest,
    decoded_token: dict = Depends(auth_exception_handler)
) -> dict:
    """
    Changes the user password.
    """

    user_id: str = decoded_token.get("sub")

    if not user_id.isalnum():
        raise HTTPException(status_code=400, detail="Invalid user ID")

    async with DbDriver(settings.db_url).get_db_session() as session:
        user_repository = UsersRepository(session)
        result = await UsersService(user_repository).change_password(
            password_change_request.new_password,
            password_change_request.new_password_match,
            password_change_request.old_password,
            int(user_id),
        )

    if not result:
        raise HTTPException(status_code=400, detail="Password not changed")

    return {"message": "Ok"}
