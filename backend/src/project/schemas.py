import datetime
from typing import Optional, List

from pydantic import BaseModel
from task.schemas import TaskSchema


class ProjectRead(BaseModel):
    id: int
    name: str
    description: str
    created_at: datetime.datetime
    organization_id: int
    asana_id: str
    tasks: Optional[List["TaskSchema"]] = None

    class Config:
        from_attributes = True


class ProjectFind(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    asana_id: Optional[str] = None


class ProjectCreate(BaseModel):
    name: str
    description: Optional[str]
    organization_id: int
    asana_id: Optional[str]


class ProjectUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    created_at: Optional[datetime.datetime] = None
    organization_id: Optional[int] = None
    asana_id: Optional[int] = None
