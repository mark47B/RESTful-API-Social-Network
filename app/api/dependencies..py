from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.config import config
from app.core import user
from app.service.store import sql

__engine: AsyncEngine | None = None


def __async_engine():
    global __engine

    if __engine is None:
        __engine = create_async_engine(
            url=config.POSTGRES_CONNECTION_STR,
            echo=config.PRJ_DEBUG_ENVIRONMENT,
        )

    return __engine


async def __sql_async_session(engine: AsyncEngine = Depends(__async_engine)):
    _async_session = sessionmaker(
        engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )
    async with _async_session() as session:
        return session


def user_store(session: AsyncSession = Depends(__sql_async_session)) -> user.Store:
    return sql.db.S
