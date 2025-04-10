import bcrypt

from interfaces.repository_interfaces.users_repository_interface import UsersRepositoryInterface


class UsersService:
    def __init__(self, users_repository: UsersRepositoryInterface):
        self._users_repository = users_repository

    async def get_user(self, user_id: int) -> dict:
        return await self._users_repository.get_user_by_id(user_id)

    async def create_user(self, user_data: dict) -> dict:
        user_data["password_hash"] = bcrypt.hashpw(user_data["password"].encode("utf-8"), bcrypt.gensalt())
        del user_data["password"]
        return await self._users_repository.create_user(user_data)

    async def login(self, username: str, password: str) -> dict:
        user = await self._users_repository.get_user_by_username(username)

        if user and bcrypt.checkpw(password.encode("utf-8"), user.password_hash):
            return user

    async def upload_image_name(self, image_name: str, user_id: int) -> str:
        return await self._users_repository.upload_image_name(image_name, user_id)

    async def get_username(self, user_id: int) -> str:
        return await self._users_repository.get_username(user_id)

    async def get_user_image_url(self, user_id: int) -> str:
        return await self._users_repository.get_user_image_url(user_id)

    async def change_password(self, new_password: str, new_password_match: str, old_password: str, user_id: int) -> bool:
        if new_password_match != new_password:
            return False

        password_hash = await self._users_repository.get_user_password_by_id(user_id)

        if password_hash and bcrypt.checkpw(old_password.encode("utf-8"), password_hash):
            new_password = bcrypt.hashpw(new_password.encode("utf-8"), bcrypt.gensalt())
            await self._users_repository.change_password(new_password, user_id)

            return True

        return False
