from typing import Optional, List
from uuid import UUID

from pydantic import BaseModel

from auth.schemas import UserRead, UserSchema
from task.schemas import TaskSchema


class GroupCreate(BaseModel):
    name: str
    user_id: UUID


class GroupRead(BaseModel):
    id: int
    name: str
    user: UserSchema
    tasks: Optional[List[TaskSchema]] = []

    class Config:
        from_attributes = True


class GroupFind(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None


class GroupUpdate(BaseModel):
    name: Optional[str] = None
    user_id: Optional[UUID] = None
