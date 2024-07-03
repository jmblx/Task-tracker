import datetime
from typing import Optional, List, Any, Dict
from uuid import UUID

from pydantic import BaseModel, Field, UUID4



class TaskBase:
    name: Optional[str] = None
    description: Optional[str] = None
    is_done: Optional[bool] = None
    added_at: Optional[datetime.datetime] = None
    done_at: Optional[datetime.datetime] = None
    assigner_id: Optional[UUID] = None
    color: Optional[str] = None
    duration: Optional[datetime.timedelta] = Field(default_factory=datetime.timedelta)
    difficulty: Optional[str] = None
    project_id: Optional[int] = None
    group_id: Optional[int] = None


class TaskSchema(TaskBase, BaseModel):
    id: int
    description: str
    is_done: bool
    added_at: Optional[datetime.datetime] = None
    done_at: Optional[datetime.datetime] = None
    color: str
    difficulty: str

    class Config:
        from_attributes = True


def get_user_read():
    from auth.schemas import UserRead
    return UserRead

class UserAssignee(BaseModel):
    id: Optional[UUID]
    organization_id: Optional[int]
    github_data: Optional[Dict[str, Any]] = None
    class Config:
        from_attributes = True


class TaskUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    is_done: Optional[bool] = None
    added_at: Optional[datetime.datetime] = None
    done_at: Optional[datetime.datetime] = None
    assigner_id: Optional[UUID4] = None
    color: Optional[str] = None
    duration: Optional[datetime.timedelta] = Field(default_factory=datetime.timedelta)
    difficulty: Optional[str] = None
    project_id: Optional[int] = None
    group_id: Optional[int] = None


    class Config:
        from_attributes = True
        arbitrary_types_allowed = True


class TaskFind(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    assigner_id: Optional[UUID] = None
    color: Optional[str] = None
    difficulty: Optional[str] = None
    project_id: Optional[int] = None
    group_id: Optional[int] = None

    class Config:
        from_attributes = True
