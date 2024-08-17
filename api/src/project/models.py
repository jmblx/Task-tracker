from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.database import Base
from db_types import added_at, intpk
from organization.models import Organization


class Project(Base):
    __tablename__ = "project"

    id: Mapped[intpk]
    name: Mapped[str]
    description: Mapped[str]
    created_at: Mapped[added_at]
    tasks = relationship(
        "Task",
        back_populates="project",
        uselist=True,
        cascade="all, delete-orphan",
    )
    organization_id: Mapped[int] = mapped_column(
        ForeignKey("organization.id", ondelete="CASCADE")
    )
    organization: Mapped["Organization"] = relationship(
        "Organization", uselist=False, back_populates="projects"
    )
    groups = relationship(
        "Group",
        back_populates="project",
        uselist=True,
        cascade="all, delete-orphan",
    )
    # asana_id: Mapped[str]
