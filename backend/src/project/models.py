from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, relationship, mapped_column

from database import Base
from my_type_notation import intpk, added_at
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
    )
    organization_id: Mapped[int] = mapped_column(ForeignKey("organization.id"))
    organization: Mapped["Organization"] = relationship("Organization", uselist=False, back_populates="projects")
    asana_id: Mapped[str]

