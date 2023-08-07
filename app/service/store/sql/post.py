from datetime import datetime
from uuid import UUID

from sqlalchemy import delete, select

from app.core.post import store
from app.core.post.schemas import Post, PostCreate, PostPatch

from ..models import EstimationModel, TimeStampModel, UUIDModel
from .db import async_session_maker


class Table(UUIDModel, TimeStampModel, EstimationModel, table=True):
    __tablename__: str = "posts"
    title: str
    content: str


def fromPost(data: Post) -> Table:
    return Table(**data.dict())


def fromPostCreate(data: PostCreate) -> Table:
    return Table(**data.dict())


def to_Post(row: Table) -> Post:
    return Post(**row.dict())


# Возможно плохо создавать сессию с БД на каждый запрос, нужно исправить
class Store(store.Store):
    async def create(self, data: PostCreate) -> UUID | None:
        async with async_session_maker() as session:
            row = fromPostCreate(data=data)
            session.add(row)
            await session.commit()
            return row.uuid

    async def get_post_uuid(self, uuid: UUID) -> Post | None:
        async with async_session_maker() as session:
            stmt = select(Table).where(Table.uuid == uuid)
            result = await session.execute(stmt)
            row = result.scalar_one_or_none()
            if row is None:
                return None
            return to_Post(row)

    async def patch_post_uuid(self, uuid: UUID, data: PostPatch) -> Post | None:
        async with async_session_maker() as session:
            stmt = select(Table).where(Table.uuid == uuid)
            result = await session.execute(stmt)
            row = result.scalar_one_or_none()
            row.__setattr__("updated_at", datetime.now())
            if row:
                for key, value in data.dict().items():
                    setattr(row, key, value)
                await session.commit()
                return to_Post(row)
            return None

    async def delete_post_uuid(self, uuid: UUID) -> bool | None:
        async with async_session_maker() as session:
            if await session.get(Table, uuid) is None:
                return None
            stmt = delete(Table).where(Table.uuid == uuid)
            await session.execute(stmt)
            await session.commit()
            return True
