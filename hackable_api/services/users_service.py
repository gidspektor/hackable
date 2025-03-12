import bcrypt

from interfaces.repository_interfaces.users_repository_interface import UsersRepositoryInterface


class UsersService:
    def __init__(self, users_repository: UsersRepositoryInterface):
        self._users_repository = users_repository

    async def get_user(self, user_id: int) -> UsersRepositoryInterface:
        return await self._users_repository.get_user_by_id(user_id)

    async def create_user(self, user_data: dict) -> UsersRepositoryInterface:
        user_data.password = bcrypt.hashpw(user_data.password.encode('utf-8'), bcrypt.gensalt())
        return await self._users_repository.create_user(user_data)

    async def login(self, username: str, password: str) -> UsersRepositoryInterface:
        user = await self._users_repository.get_user_by_username(username)

        if user and bcrypt.checkpw(password.encode('utf-8'), user.password_hash.encode('utf-8')):
            return user

    async def upload_image_name(self, image_name: str, user_id: int) -> str:
        return await self._users_repository.upload_image_name(image_name, user_id)
