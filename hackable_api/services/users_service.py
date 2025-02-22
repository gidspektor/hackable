import bcrypt

from hackable_api.interfaces.repository_interfaces.users_repository_interface import UsersRepositoryInterface


class UsersService:
    def __init__(self, users_repository: UsersRepositoryInterface):
        self._users_repository = users_repository

    def get_user(self, user_id: int) -> UsersRepositoryInterface:
        return self._users_repository.get_user(user_id)

    def create_user(self, username: str, password: str) -> UsersRepositoryInterface:
        hased_password = bcrypt.hashpw(password.encode('utf-8'))
        return self._users_repository.create_user(username, hased_password)

    def login(self, username: str, password: str) -> UsersRepositoryInterface:
        # ideal code to combat injection and not just directly return the db response
        # user = self._users_repository.get_user(username)
        #if bcrypt.checkpw(password.encode('utf-8'), user['password']):
        #    return user
        #return None

        password = bcrypt.hashpw(password.encode('utf-8'))
        user = self._users_repository.get_user(username, password)

        return user
