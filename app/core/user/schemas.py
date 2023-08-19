from pydantic import BaseModel, SecretStr

from app.core.schemas import TimeStampModel, UUIDModel
from app.core.user.examples import ex_user_create, ex_user_patch, ex_user_read


class UserBase(BaseModel):
    nickname: str
    email: str


class Identity(BaseModel):
    email: str
    password: SecretStr


class User(UUIDModel, TimeStampModel):
    baseInfo: UserBase
    identity: Identity


class UserRead(UserBase, UUIDModel, TimeStampModel):  # DTO -- Data Transfer Object
    class Config:
        schema_extra = {"example": ex_user_read}


class UserCreate(UserBase, Identity):
    class Config:
        schema_extra = {"example": ex_user_create}


class UserPatch(BaseModel):
    nickname: str

    class Config:
        schema_extra = {"example": ex_user_patch}
