from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class UUIDModel(BaseModel):
    uuid: UUID


class TimeStampModel(BaseModel):
    created_at: datetime
    updated_at: datetime


class EstimationModel(BaseModel):
    likes: int
    dislikes: int
    views: int


class StatusMessage(BaseModel):
    status: bool
    message: str
