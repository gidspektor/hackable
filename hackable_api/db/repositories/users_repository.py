from hackable_api.interfaces.driver_interfaces.db_driver_interface import DbDriverInterface
from hackable_api.interfaces.repository_interfaces.users_repository_interface import UsersRepositoryInterface


class UsersRepository(UsersRepositoryInterface):
    def __init__(self, db_driver: DbDriverInterface):
        self._db = db_driver

    def create_user(self, user):
        self._db.users.insert_one(user)

    def get_user(self, username):
        return self._db.users.find_one({'username': username})
