from sqlalchemy.future import select, update

from interfaces.driver_interfaces.db_driver_interface import DbDriverInterface
from interfaces.repository_interfaces.users_repository_interface import UsersRepositoryInterface

from db.models.users import Users

class UsersRepository(UsersRepositoryInterface):
    def __init__(self, db_driver: DbDriverInterface):
        self._db = db_driver

    async def create_user(self, username: str, hashed_password: str) -> Users:
        new_user = Users(
            username=username,
            password=hashed_password,
        )

        self._db.add(new_user)

        await self._db.commit()

        await self._db.refresh(new_user)

        return new_user

    async def get_user(self, user_id: int) -> Users:
        stmt = select(Users).where(Users.id == user_id)

        result = await self._db.execute(stmt).first()

        return result

    async def upload_image_name(self, image_name: str, user_id: int) -> Users|bool:
        stmt = update(Users).where(Users.id == user_id).values(image_name=image_name)
        result = await self._db.execute(stmt)
        await self._db.commit()

        if result.rowcount == 0:
            return False
        
        return result
