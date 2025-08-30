from typing import AsyncIterator

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
)

from .settings import settings

async_engine = create_async_engine(settings.API_DATABASE_URL)


async def get_async_session() -> AsyncIterator[AsyncSession]:
    async with AsyncSession(async_engine, expire_on_commit=False) as session:
        yield session
