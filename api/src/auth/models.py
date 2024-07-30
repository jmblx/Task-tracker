from datetime import datetime
from typing import List
from uuid import uuid4, UUID

from sqlalchemy import ForeignKey, String
from sqlalchemy.dialects.postgresql import JSON, BYTEA
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base
from my_type_notation import added_at, intpk
from task.models import UserTask, Task, Group  # noqa


class User(Base):
    __tablename__ = "user"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    first_name: Mapped[str]
    last_name: Mapped[str]
    role_id: Mapped[int] = mapped_column(ForeignKey("role.id"), default=1)
    role: Mapped["Role"] = relationship(back_populates="users", uselist=False)
    email: Mapped[str]
    is_email_confirmed: Mapped[bool] = mapped_column(default=False)
    email_confirmation_token = mapped_column(nullable=True, type_=String(50))
    registered_at: Mapped[added_at]
    hashed_password: Mapped[bytes] = mapped_column(BYTEA, nullable=True)
    # phone_number: Mapped[str] = mapped_column(VARCHAR(12), nullable=True)
    is_active: Mapped[bool] = mapped_column(default=True)
    is_verified: Mapped[bool] = mapped_column(default=True)
    tg_id: Mapped[str] = mapped_column(String(20), nullable=True, unique=True)
    tg_settings: Mapped[dict] = mapped_column(JSON, nullable=True)
    tasks = relationship(
        "Task", back_populates="assignees", uselist=True, secondary="user_task"
    )
    task_created = relationship("Task", back_populates="assigner", uselist=True)
    organization_id: Mapped[int] = mapped_column(
        ForeignKey("organization.id"), nullable=True
    )
    organization = relationship("Organization", back_populates="staff", uselist=False)
    pathfile: Mapped[str] = mapped_column(nullable=True)
    # oauth_accounts: Mapped[List[OAuthAccount]] = relationship(
    #     "OAuthAccount"
    # )
    groups: Mapped[List["Group"]] = relationship(
        "Group", uselist=True, back_populates="user"
    )
    github_name: Mapped[str] = mapped_column(nullable=True)
    refresh_tokens: Mapped[List["RefreshToken"]] = relationship(
        "RefreshToken", uselist=True
    )


class Role(Base):
    __tablename__ = "role"

    id: Mapped[intpk]
    name: Mapped[str] = mapped_column(nullable=False)
    permissions: Mapped[dict] = mapped_column(JSON)
    users: Mapped[List["User"]] = relationship(back_populates="role", uselist=True)


class RefreshToken(Base):
    __tablename__ = "refresh"

    id: Mapped[UUID] = mapped_column(primary_key=True)
    user_id: Mapped[UUID] = mapped_column(ForeignKey("user.id"))
    user: Mapped[User] = relationship(back_populates="refresh_tokens")
    fingerprint: Mapped[str]
    expires_in: Mapped[datetime]
    created_at: Mapped[added_at]