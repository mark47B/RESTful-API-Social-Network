from typing import Any, Protocol
from uuid import UUID

from app.core.user.schemas import Identity, User, UserBase, UserCreate, UserPatch


class Store(Protocol):
    async def create(self, data: UserCreate) -> UUID:
        ...

    async def get_user_uuid(self, uuid: UUID) -> User | None:
        ...

    async def get_user_email(self, email: str) -> User | None:
        ...

    async def get_baseInfo_uuid(self, uuid: UUID) -> UserBase | None:
        ...

    async def get_identity_uuid(self, uuid: UUID) -> Identity | None:
        ...

    async def delete_user_uuid(self, uuid: UUID) -> Any:
        ...

    async def delete_user_email(self, email: str) -> Any:
        ...

    async def patch_user_uuid(self, uuid: UUID, data: UserPatch) -> UserBase:
        ...

    async def patch_user_email(self, uuid: UUID, data: UserPatch) -> UserBase:
        ...
