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

    async def get_session(self) -> AsyncGenerator[AsyncSession, None]:
        try:
            async with self.session_factory() as session:
                yield session
        finally:
            await session.close()

    def get_scoped_session(self):
        session = async_scoped_session(
            session_factory=self.session_factory,
            scopefunc=asyncio.current_task,
        )
        return session

    async def session_dependency(self):
        async with self.session_factory() as session:
            yield session
            await session.close()

    async def scoped_session_dependency(self):
        session = self.get_scoped_session()
        yield session
        await session.close()

db_helper = DatabaseHelper(settings.DATABASE_URL)
