from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, relationship, mapped_column

from core.db.database import Base
from core.db.db_types import intpk


class Group(Base):
    __tablename__ = "group"

    id: Mapped[intpk]
    name: Mapped[str]
    tasks = relationship(
        "Task",
        uselist=True,
        back_populates="group",
        cascade="all, delete-orphan",
    )
    user = relationship("User", uselist=False, back_populates="groups")
    user_id: Mapped[UUID] = mapped_column(ForeignKey("user.id"), nullable=True)
    project = relationship("Project", uselist=False, back_populates="groups")
    project_id: Mapped[int] = mapped_column(
        ForeignKey("project.id"), nullable=True
    )
