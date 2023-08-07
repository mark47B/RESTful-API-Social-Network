from typing import Protocol

from .schemas import Post, PostCreate, PostPatch


class Store(Protocol):
    async def create(self, title: str, data: PostCreate) -> Post:
        ...

    async def get_post_uuid(self, uuid: str) -> Post:
        ...

    async def patch_post_uuid(self, uuid: str, data: PostPatch) -> Post:
        ...

    async def delete_post_uuid(self, uuid: str) -> bool:
        ...
