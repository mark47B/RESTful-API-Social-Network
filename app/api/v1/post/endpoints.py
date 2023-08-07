from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Response, status

from app.core.post.schemas import Post, PostCreate, PostPatch
from app.service.store.sql import post as postModule

from .dependencies import get_post_crud

router = APIRouter(prefix="/post", tags=["post"])


@router.get("/{uuid}", response_model=Post, status_code=status.HTTP_200_OK)
async def get_post_uuid(
    uuid: str, postCRUD: postModule.Store = Depends(get_post_crud)
) -> Response:
    post = await postCRUD.get_post_uuid(uuid=UUID(uuid))
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The post with UUID={uuid} hasn't been found!",
        )
    return Response(status_code=status.HTTP_200_OK, content=post.json())


@router.post("", response_model=Post, status_code=status.HTTP_201_CREATED)
async def create_post(
    data: PostCreate, postCRUD: postModule.Store = Depends(get_post_crud)
) -> Response:
    uuid = await postCRUD.create(data=data)
    return Response(status_code=status.HTTP_201_CREATED, content=uuid.__str__())


@router.patch("/{uuid}", response_model=Post, status_code=status.HTTP_200_OK)
async def patch_post_uuid(
    uuid: str, data: PostPatch, postCRUD: postModule.Store = Depends(get_post_crud)
):
    patched_post = await postCRUD.patch_post_uuid(uuid=UUID(uuid), data=data)
    if patched_post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The post with UUID={uuid} hasn't been found!",
        )
    return Response(status_code=status.HTTP_200_OK, content=patched_post.json())


@router.delete("/{uuid}", status_code=status.HTTP_200_OK)
async def delete_post_uuid(
    uuid: str, postCRUD: postModule.Store = Depends(get_post_crud)
):
    result = await postCRUD.delete_post_uuid(uuid=UUID(uuid))
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The post with UUID={uuid} hasn't been found!",
        )
    return Response(status_code=status.HTTP_200_OK, content=result.__str__())
