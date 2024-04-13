import datetime
from typing import Optional

from pydantic import BaseModel


class ProjectRead(BaseModel):
    id: int
    name: str
    description: str
    created_at: datetime.datetime
    organization_id: int
    asana_id: str

    class Config:
        from_attributes = True


class ProjectFind(BaseModel):
    id: int
    name: str
    asana_id: str


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
