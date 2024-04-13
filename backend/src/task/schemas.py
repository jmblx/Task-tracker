import datetime
from typing import Optional, List

from pydantic import BaseModel

from auth.schemas import UserRead, UserSchema
from task.models import Difficulty


class TaskBase:
    name: Optional[str]
    description: Optional[str]
    is_done: Optional[bool]
    added_at: Optional[datetime.datetime]
    done_at: Optional[datetime.datetime]
    assigner_id: Optional[int]
    color: Optional[str]
    duration: Optional[datetime.datetime]
    difficulty: Optional[str]
    project_id: Optional[int]


class TaskCreate(BaseModel):
    name: str
    description: Optional[str]
    is_done: Optional[bool]
    added_at: Optional[datetime.datetime] = None
    done_at: Optional[datetime.datetime] = None
    assigner_id: int
    color: Optional[str] = None
    duration: datetime.datetime
    difficulty: Optional[str] = None
    project_id: int


class TaskRead(TaskCreate):
    id: int
    description: str
    is_done: bool
    added_at: datetime.datetime
    done_at: datetime.datetime
    color: str
    difficulty: str
    assignees: Optional[List["UserSchema"]] = None
    assigner: Optional["UserSchema"] = None


class TaskUpdate(TaskBase, BaseModel):
    pass


class TaskFind(TaskBase, BaseModel):
    id: int
