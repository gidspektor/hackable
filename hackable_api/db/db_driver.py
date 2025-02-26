from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from interfaces.driver_interfaces.db_driver_interface import DbDriverInterface


class DbDriver(DbDriverInterface):
    def __init__(self, db_url: str):
        # Create a single engine instance for reuse
        self.engine = create_async_engine(db_url)

        # Create a session factory that generates new sessions
        self.session_factory = sessionmaker(
            bind=self.engine,
            class_=AsyncSession,
            expire_on_commit=False
        )

    @asynccontextmanager
    async def get_db_session(self) -> AsyncSession:
        """Provides an async database session."""

        async with self.session_factory() as session:
            try:
                yield session
                await session.commit()
            except Exception:
                await session.rollback()
                raise
            finally:
                await session.close()

    async def close(self):
        """Properly dispose of the engine when shutting down the app."""
        await self.engine.dispose()
