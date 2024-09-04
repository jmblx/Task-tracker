from uuid import UUID, uuid4

from sqlalchemy import ForeignKey, String
from sqlalchemy.dialects.postgresql import BYTEA, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.db.database import Base
from core.db.db_types import added_at
from domain.entities.organization.models import Organization


class User(Base):
    __tablename__ = "user"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    first_name: Mapped[str]
    last_name: Mapped[str]
    role_id: Mapped[int] = mapped_column(ForeignKey("role.id"), default=1)
    role = relationship("Role", back_populates="users", uselist=False)
    email: Mapped[str]
    is_email_confirmed: Mapped[bool] = mapped_column(default=False)
    email_confirmation_token = mapped_column(nullable=True, type_=String(50))
    registered_at: Mapped[added_at]
    hashed_password: Mapped[bytes] = mapped_column(BYTEA, nullable=True)
    # hashed_password: Mapped[str] = mapped_column(String(50))
    # phone_number: Mapped[str] = mapped_column(VARCHAR(12), nullable=True)
    is_active: Mapped[bool] = mapped_column(default=True)
    is_verified: Mapped[bool] = mapped_column(default=True)
    tg_id: Mapped[str] = mapped_column(String(20), nullable=True, unique=True)
    tg_settings: Mapped[dict] = mapped_column(JSON, nullable=True)
    tasks = relationship(
        "Task", back_populates="assignees", uselist=True, secondary="user_task"
    )
    task_created = relationship(
        "Task",
        back_populates="assigner",
        uselist=True,
        cascade="all, delete-orphan",
    )
    organizations: Mapped["Organization"] = relationship(
        "Organization",
        back_populates="staff",
        uselist=True,
        secondary="user_org",
    )
    pathfile: Mapped[str] = mapped_column(nullable=True)
    groups = relationship(
        "Group",
        uselist=True,
        back_populates="user",
        cascade="all, delete-orphan",
    )
    github_name: Mapped[str] = mapped_column(nullable=True)
