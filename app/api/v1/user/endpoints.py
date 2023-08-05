from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from fastapi import status
from fastapi import status as http_status

from app.core.schemas import StatusMessage
from app.core.user.schema import UserCreate, UserPatch, UserRead
from app.service.store.sql.user import UserCRUD

from .dependencies import get_user_crud

router = APIRouter(prefix="/user", tags=["user"])


@router.get(
    "/{user_uuid}", response_model=UserRead | None, status_code=status.HTTP_200_OK
)
async def get_user_uuid(
    user_uuid: str, userCRUD_session: UserCRUD = Depends(get_user_crud)
):
    user = await userCRUD_session.get_by_uuid(uuid=UUID(user_uuid))

    if user is None:
        raise HTTPException(
            status_code=http_status.HTTP_404_NOT_FOUND,
            detail=f"The user with UUID={user_uuid} hasn't been found!",
        )

    return user


# @router.get("/{email}", response_model=UserRead, status_code=status.HTTP_200_OK)
# async def get_user_by_email(
#     email: str, userCRUD_session: UserCRUD = Depends(get_user_crud)
# ):
#     user = await userCRUD_session.get_by_email(email=email)
# if user is None:
#     raise HTTPException(
#         status_code=http_status.HTTP_404_NOT_FOUND,
#         detail=f"The user with email={email} hasn't been found!",
#     )

#     return user


@router.post("", status_code=status.HTTP_201_CREATED)
async def create(data: UserCreate, userCRUD_session: UserCRUD = Depends(get_user_crud)):
    user = await userCRUD_session.create(data=data)
    return user


@router.patch(
    "/{user_uuid}", response_model=StatusMessage, status_code=status.HTTP_200_OK
)
async def patch_user_uuid(
    user_uuid: UUID,
    data: UserPatch,
    userCRUD_session: UserCRUD = Depends(get_user_crud),
):
    user = await userCRUD_session.patch_by_uuid(uuid=user_uuid, data=data)
    if user:
        raise HTTPException(
            status_code=http_status.HTTP_404_NOT_FOUND,
            detail=f"The user with UUID={user_uuid} hasn't been found!",
        )
    return status


@router.delete("/{user_uuid}", status_code=status.HTTP_200_OK)
async def delete_user_uuid(
    user_uuid: str, userCRUD_session: UserCRUD = Depends(get_user_crud)
):
    status = await userCRUD_session.delete_by_uuid(uuid=UUID(user_uuid))

    return status
