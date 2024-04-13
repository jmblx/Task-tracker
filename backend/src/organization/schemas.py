from typing import Optional, List

from pydantic import BaseModel
from auth.schemas import UserRead


class OrganizationCreate(BaseModel):
    name: str
    description: str


class OrganizationRead(OrganizationCreate):
    id: int
    workers: Optional[List["UserRead"]]
    managers: Optional[List["UserRead"]]

    class Config:
        from_attributes = True


class OrganizationFind(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None


class OrganizationUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
