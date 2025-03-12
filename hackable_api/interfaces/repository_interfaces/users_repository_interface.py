from abc import ABC, abstractmethod

from db.models.users import Users

class UsersRepositoryInterface(ABC):
    @abstractmethod
    def create_user(self, user_data: dict) -> Users:
        raise NotImplementedError("This method should be overridden by subclasses")

    @abstractmethod
    def get_user_by_id(self, user_id: int) -> Users:
        raise NotImplementedError("This method should be overridden by subclasses")
    
    @abstractmethod
    def get_user_by_username(self, user_id: int) -> Users:
        raise NotImplementedError("This method should be overridden by subclasses")

    @abstractmethod
    def upload_image_name(self, image_name: str, user_id: int) -> Users:
        raise NotImplementedError("This method should be overridden by subclasses")
