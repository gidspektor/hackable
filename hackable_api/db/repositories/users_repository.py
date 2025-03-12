from sqlalchemy import select, update

from interfaces.driver_interfaces.db_driver_interface import DbDriverInterface
from interfaces.repository_interfaces.users_repository_interface import UsersRepositoryInterface

from db.models.users import Users

class UsersRepository(UsersRepositoryInterface):
    def __init__(self, db_driver: DbDriverInterface):
        self._db = db_driver

    async def create_user(self, user_data: dict) -> Users:
        new_user = Users(**user_data)  # 🚨 Directly unpacking user input
        self._db.add(new_user)
        await self._db.commit()
        return new_user

    async def get_user_by_id(self, user_id: int) -> Users:
        stmt = select(Users).where(Users.id == user_id)

        result = await self._db.execute(stmt)

        return result.scalar_one_or_none()
    
    async def get_user_by_username(self, username: str) -> Users:
        stmt = select(Users).where(Users.username == username)

        result = await self._db.execute(stmt)
        user = result.scalar_one_or_none()

        return user

    async def upload_image_name(self, image_name: str, user_id: int) -> Users|bool:
        stmt = update(Users).where(Users.id == user_id).values(image_name=image_name)
        result = await self._db.execute(stmt)
        await self._db.commit()

        if result.rowcount == 0:
            return False
        
        return result
