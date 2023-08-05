from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.service.store.sql.db import get_async_session
from app.service.store.sql.user import UserCRUD


async def get_user_crud(
    session: AsyncSession = Depends(get_async_session),
) -> UserCRUD:
    return UserCRUD()
