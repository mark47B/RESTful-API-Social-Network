from typing import Any

from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel.ext.asyncio.session import AsyncSession

from app.config import config

db_connection_str = config.POSTGRES_CONNECTION_STR

async_engine = create_async_engine(
    db_connection_str, echo=config.PRJ_DEBUG_ENVIRONMENT, future=True
)
async_session_maker = sessionmaker(
    bind=async_engine, class_=AsyncSession, expire_on_commit=False
)


async def get_async_session() -> AsyncSession | Any:
    async with async_session_maker() as session:
        yield session
