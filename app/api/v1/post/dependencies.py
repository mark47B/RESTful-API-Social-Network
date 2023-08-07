from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.service.store.sql.db import get_async_session
from app.service.store.sql.post import Store


async def get_post_crud(
    session: AsyncSession = Depends(get_async_session),
) -> Store:
    return Store()
