from typing import AsyncGenerator, Generator

from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy.orm.session import Session, sessionmaker

from app.config import settings

# Create an async engine
async_engine = create_async_engine(str(settings.PG_DSN), echo=True)
async_session = async_sessionmaker(async_engine)


async def get_async_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as db:
        try:
            yield db
        finally:
            await db.close()


engine = create_engine(str(settings.PG_DSN), echo=True)
session = sessionmaker(engine)


def get_db() -> Generator[Session, None, None]:
    with session() as db:
        try:
            yield db
        finally:
            db.close()
