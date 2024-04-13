from typing import Optional

from pydantic import BaseModel


class OrganizationCreate(BaseModel):
    name: str
    description: str


class OrganizationRead(OrganizationCreate):
    id: int

    class Config:
        from_attributes = True


class OrganizationFind(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None


class OrganizationUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
