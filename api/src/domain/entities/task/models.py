import datetime
import enum

from sqlalchemy import ForeignKey, Interval
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.db.database import Base
from core.db.db_types import added_at, intpk


class Difficulty(enum.Enum):
    easy = "Легкая"
    medium = "Средняя"
    hard = "Сложная"
    challenging = "Требующая усилий"
    complex = "Сложная"  # noqa: PIE796


class Task(Base):
    __tablename__ = "task"

    id: Mapped[intpk]
    name: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=False)
    is_done: Mapped[bool] = mapped_column(nullable=False, default=False)
    added_at: Mapped[added_at]
    end_date: Mapped[datetime.datetime] = mapped_column(nullable=True)
    done_at: Mapped[datetime.datetime] = mapped_column(nullable=True)
    color: Mapped[str]
    duration = mapped_column(Interval)
    difficulty: Mapped[Difficulty] = mapped_column(nullable=True)
    #  pathfile: Mapped[str] = mapped_column(nullable=True)
    assignees = relationship(
        "User",
        back_populates="tasks",
        uselist=True,
        secondary="user_task",
    )
    assigner_id: Mapped[int] = mapped_column(
        ForeignKey("user.id", ondelete="CASCADE"), nullable=True
    )
    assigner = relationship(
        "User",
        back_populates="task_created",
        uselist=False,
    )
    project_id: Mapped[int] = mapped_column(
        ForeignKey("project.id", ondelete="CASCADE"), nullable=True
    )
    project = relationship("Project", uselist=False, back_populates="tasks")
    group_id: Mapped[int] = mapped_column(
        ForeignKey("group.id", ondelete="CASCADE"), nullable=True
    )
    group = relationship("Group", uselist=False, back_populates="tasks")


class UserTask(Base):
    __tablename__ = "user_task"

    id: Mapped[intpk]
    github_data: Mapped[dict] = mapped_column(JSON, nullable=True)
    task_id: Mapped[int] = mapped_column(
        ForeignKey("task.id", ondelete="CASCADE"), nullable=False
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey("user.id", ondelete="CASCADE"), nullable=False
    )
    is_employee: Mapped[bool] = mapped_column(nullable=False, default=True)
