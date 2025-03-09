import asyncio

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import (
    async_scoped_session,
    async_sessionmaker,
    create_async_engine,
)

from app.config import settings
from app.db import get_async_db
from app_web import app

async_engine = create_async_engine(
    str(settings.ASYNC_PG_DSN),
)
async_session = async_scoped_session(
    async_sessionmaker(
        async_engine,
        autocommit=False,
        autoflush=False,
        expire_on_commit=False,
    ),
    scopefunc=lambda: asyncio.current_task().get_name(),  # type: ignore[union-attr]
)


@pytest.fixture(autouse=True)
async def db():
    async with async_engine.connect() as connection:
        async with connection.begin() as transaction:
            session = async_session(bind=connection)

            async def override_get_db():
                yield session

            app.dependency_overrides[get_async_db] = override_get_db

            try:
                yield session
            finally:
                await transaction.rollback()


@pytest.fixture
async def client():
    # TODO: add auth to app
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        yield ac
