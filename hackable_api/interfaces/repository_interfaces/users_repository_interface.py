from abc import ABC, abstractmethod


class UsersRepositoryInterface(ABC):
    @abstractmethod
    def create_user(self, user):
        raise NotImplementedError("This method should be overridden by subclasses")

    @abstractmethod
    def get_user(self, username):
        raise NotImplementedError("This method should be overridden by subclasses")

    @abstractmethod
    def upload_image_name(self, image):
        raise NotImplementedError("This method should be overridden by subclasses")
