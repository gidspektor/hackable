from abc import ABC, abstractmethod
from typing import Dict


class UsersServiceInterface(ABC):
    @abstractmethod
    async def get_user(self, user_id: int) -> dict:
        raise NotImplementedError("This method should be overridden by subclasses")

    @abstractmethod
    async def create_user(self, user_data: Dict) -> dict:
        raise NotImplementedError("This method should be overridden by subclasses")

    @abstractmethod
    async def login(self, username: str, password: str) -> dict:
        raise NotImplementedError("This method should be overridden by subclasses")

    @abstractmethod
    async def upload_image_name(self, image_name: str, user_id: int) -> str:
        raise NotImplementedError("This method should be overridden by subclasses")

    @abstractmethod
    async def get_username(self, user_id: int) -> str:
        raise NotImplementedError("This method should be overridden by subclasses")
