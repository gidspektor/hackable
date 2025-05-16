from abc import ABC, abstractmethod
from sqlalchemy.ext.asyncio import AsyncSession


class DbDriverInterface(ABC):
    @abstractmethod
    async def get_db_session(self) -> AsyncSession:
        raise NotImplementedError("This method should be overridden by subclasses")
