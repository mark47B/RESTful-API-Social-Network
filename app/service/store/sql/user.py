from dataclasses import dataclass
from uuid import UUID

from sqlmodel import Field, delete, select

from app.core import user as userCore
from app.core.schemas import StatusMessage
from app.core.user.schemas import UserPatch, UserRead
from app.service.store.models import TimeStampModel, UUIDModel

from .db import async_session_maker


class Table(UUIDModel, TimeStampModel, table=True):
    __tablename__: str = "users"
    nickname: str
    email: str = Field(
        nullable=True, index=True, sa_column_kwargs={"unique": True}, unique=True
    )
    password: str


def from_userCreate(data: userCore.UserCreate) -> "Table":
    return Table(
        nickname=data.nickname,
        email=data.email,
        password=data.password.get_secret_value(),
    )


def to_userRead(row: Table) -> userCore.UserRead:
    return userCore.UserRead(
        uuid=row.uuid,
        nickname=row.nickname,
        email=row.email,
        created_at=row.created_at,
        updated_at=row.updated_at,
    )


def to_user(row: Table) -> userCore.User:
    return userCore.User(
        uuid=row.uuid,
        baseInfo=to_Baseinfo(row),
        identity=to_identity(row),
        created_at=row.created_at,
        updated_at=row.updated_at,
    )


def to_Baseinfo(row: Table) -> userCore.UserBase:
    return userCore.UserBase(**row.dict(include={"nickname"}))


def to_identity(row: Table) -> userCore.Identity:
    return userCore.Identity(**row.dict(include={"password", "email"}))


class UserCRUD(userCore.Store):
    async def create(self, data: userCore.UserCreate) -> UUID:
        async with async_session_maker() as session:
            row: Table = from_userCreate(data)
            session.add(row)
            await session.commit()
            return row.uuid

    async def get_user_uuid(self, uuid: UUID) -> userCore.UserRead | None:
        async with async_session_maker() as session:
            stmt = select(Table).where(Table.uuid == uuid)
            result = await session.execute(stmt)
            row = result.scalar_one_or_none()
            if row is None:
                return None
            return to_userRead(row._mapping["Table"])

    async def get_user_email(self, email: str) -> userCore.User | None:
        async with async_session_maker() as session:
            stmt = select(Table).where(Table.email == email)
            result = await session.execute(stmt)
            record = result.first()

            if record is None:
                return None

            return to_user(record._mapping["Table"])

    async def get_identity_uuid(self, uuid: UUID) -> userCore.Identity | None:
        async with async_session_maker() as session:
            stmt = select(Table).where(Table.uuid == uuid)
            result = await session.execute(stmt)
            row = result.scalar_one_or_none()
            if row is None:
                return None
            return to_user(row=row).identity

    async def get_baseInfo_uuid(self, uid: UUID) -> userCore.UserBase | None:
        async with async_session_maker() as session:
            stmt = select(Table).where(Table.uuid == uuid)
            result = await session.execute(stmt)
            row = result.scalar_one_or_none()
            if row is None:
                return None
            return to_user(row=row).baseInfo

    async def delete_user_uuid(self, uuid: UUID) -> bool | None:
        async with async_session_maker() as session:
            if await session.get(Table, uuid) is None:
                return None
            stmt = delete(Table).where(Table.uuid == uuid)
            await session.execute(stmt)
            await session.commit()
            return True

    async def delete_user_email(self, email: str) -> StatusMessage:
        async with async_session_maker() as session:
            stmt = delete(Table).where(Table.email == email)
            await session.execute(statement=stmt)
            await session.commit()

            return StatusMessage(
                status=True, message=f"User with email {email} has been deleted"
            )

    async def patch_user_uuid(self, uuid: UUID, data: UserPatch) -> UserRead | None:
        async with async_session_maker() as session:
            stmt = select(Table).where(Table.uuid == uuid)
            result = await session.execute(stmt)
            user = result.scalar_one_or_none()
            if user:
                for key, value in data.dict().items():
                    setattr(user, key, value)
                await session.commit()
                return to_userRead(user)
            return None

    async def patch_user_email(
        self, email: str, data: userCore.UserPatch
    ) -> UserRead | None:
        async with async_session_maker() as session:
            stmt = select(Table).where(Table.email == email)
            result = await session.execute(stmt)
            user = result.scalar_one_or_none()
            if user:
                for key, value in data.dict():
                    setattr(user, key, value)
                await session.commit()
                return to_userRead(user)
            return None
