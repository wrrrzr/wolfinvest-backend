from typing import AsyncGenerator

import pytest
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
    async_sessionmaker,
)
from sqlalchemy.pool import NullPool

from app.adapters.sqlalchemy.models import Base
from config import load_test_sqlalchemy_config

engine = create_async_engine(
    load_test_sqlalchemy_config().db_uri, poolclass=NullPool
)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)
Base.metadata.bind = engine


@pytest.fixture(scope="function")
async def session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


@pytest.fixture(autouse=True, scope="session")
async def prepare_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
