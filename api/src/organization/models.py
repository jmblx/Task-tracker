from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.orm import Mapped, relationship, mapped_column

from db.database import Base
from db_types import intpk


class Organization(Base):
    __tablename__ = "organization"

    id: Mapped[intpk]
    name: Mapped[str]
    description: Mapped[str]
    staff = relationship(
        "User", uselist=True, back_populates="organizations", secondary="user_org"
    )
    projects = relationship(
        "Project",
        uselist=True,
        back_populates="organization",
        cascade="all, delete-orphan",
    )


class UserOrg(Base):
    __tablename__ = "user_org"

    id: Mapped[intpk]
    user_id: Mapped[UUID] = mapped_column(ForeignKey("user.id", ondelete="CASCADE"))
    organization_id: Mapped[int] = mapped_column(
        ForeignKey("organization.id", ondelete="CASCADE")
    )
    position: Mapped[str]
    permissions: Mapped[dict] = mapped_column(JSON)
