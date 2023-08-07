from pydantic import BaseModel

from ..schemas import EstimationModel, TimeStampModel, UUIDModel
from .examples import ex_post_create, ex_post_patch, ex_post_read


class PostBase(BaseModel):
    title: str
    content: str


class Post(UUIDModel, PostBase, EstimationModel, TimeStampModel):
    class Config:
        schema_extra = {"example": ex_post_read}


class PostPatch(PostBase):
    class Config:
        schema_extra = {"example": ex_post_patch}


class PostCreate(PostBase):
    class Config:
        schema_extra = {"example": ex_post_create}
