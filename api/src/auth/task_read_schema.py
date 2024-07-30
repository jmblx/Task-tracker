import datetime
from typing import Optional, Any, List, Dict
from uuid import UUID

from pydantic import BaseModel, Field
from auth.schemas import UserRead


class TaskRead(BaseModel):
    name: str
    description: Optional[str]
    is_done: Optional[bool]
    added_at: Optional[datetime.datetime] = None
    done_at: Optional[datetime.datetime] = None
    assigner_id: UUID
    color: Optional[str] = None
    duration: datetime.timedelta = Field(default_factory=datetime.timedelta)
    difficulty: Optional[str] = None
    project_id: int
    group_id: Optional[int] = None
    github_data: Optional[Dict[str, Any]] = None
    id: int
    description: str
    is_done: bool
    added_at: datetime.datetime
    done_at: Optional[datetime.datetime]
    color: str
    difficulty: str
    assignees: Optional[List["UserRead"]] = None
    assigner: Optional["UserRead"] = None

    class Config:
        from_attributes = True
