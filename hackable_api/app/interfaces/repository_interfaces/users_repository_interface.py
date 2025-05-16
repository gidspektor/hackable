from abc import ABC, abstractmethod

from app.db.models.users import Users


class UsersRepositoryInterface(ABC):
    @abstractmethod
    async def create_user(self, user_data: dict) -> Users:
        raise NotImplementedError("This method should be overridden by subclasses")

    @abstractmethod
    async def get_user_by_id(self, user_id: int) -> Users:
        raise NotImplementedError("This method should be overridden by subclasses")

    @abstractmethod
    async def get_user_by_username(self, username: str) -> Users:
        raise NotImplementedError("This method should be overridden by subclasses")

    @abstractmethod
    async def upload_image_name(self, image_name: str, user_id: int) -> Users:
        raise NotImplementedError("This method should be overridden by subclasses")

    @abstractmethod
    async def get_username(self, user_id: int) -> str:
        raise NotImplementedError("This method should be overridden by subclasses")

    @abstractmethod
    async def get_user_image_url(self, user_id: int) -> str:
        raise NotImplementedError("This method should be overridden by subclasses")

    @abstractmethod
    async def change_password(self, new_password: str, user_id: int) -> bool:
        raise NotImplementedError("This method should be overridden by subclasses")

    @abstractmethod
    async def get_user_password_by_id(self, user_id: int) -> Users:
        raise NotImplementedError("This method should be overridden by subclasses")
