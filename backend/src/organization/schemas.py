from typing import Optional, List

from pydantic import BaseModel
from auth.schemas import UserRead
from project.schemas import ProjectRead


class OrganizationCreate(BaseModel):
    name: str
    description: str


class OrganizationRead(OrganizationCreate):
    id: int
    workers: Optional[List["UserRead"]]
    managers: Optional[List["UserRead"]]
    projects: Optional[List["ProjectRead"]]

    class Config:
        from_attributes = True


class OrganizationFind(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None


class OrganizationUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
