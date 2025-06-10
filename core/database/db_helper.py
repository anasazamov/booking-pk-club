from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker, async_scoped_session
from core.config import settings
import asyncio
from typing import AsyncGenerator

class DatabaseHelper:
    def __init__(self, database_url: str):
        self.engine = create_async_engine(database_url, echo=True)
        self.session_factory = async_sessionmaker(
            bind=self.engine,
            expire_on_commit=False,
            class_=AsyncSession
        )

    async def get_session(self) -> AsyncGenerator[AsyncSession]:
        try:
            async with self.session_factory() as session:
                yield session
        finally:
            await session.close()

    async def get_scoped_session(self) -> AsyncGenerator[AsyncSession]:
        async with async_scoped_session(self.session_factory, scopefunc=asyncio.current_task) as session:
            yield session

    def session_dependency(self) -> AsyncGenerator[AsyncSession]:
        """
        Dependency to be used in FastAPI routes for getting a database session.
        """
        return self.get_session()
    
    def scoped_session_dependency(self) -> AsyncGenerator[AsyncSession]:
        """
        Dependency to be used in FastAPI routes for getting a scoped database session.
        """
        return self.get_scoped_session()

# Initialize the database helper with the database URL from settings
db_helper = DatabaseHelper(settings.DATABASE_URL)
