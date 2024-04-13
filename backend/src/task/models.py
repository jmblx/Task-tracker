import datetime
import enum

from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base
from my_type_notation import added_at, intpk
from project.models import Project # noqa


class Difficulty(enum.Enum):
    easy = "Легкая"
    medium = "Средняя"
    hard = "Сложная"
    challenging = "Требующая усилий"
    complex = "Сложная"


class Task(Base):
    __tablename__ = "task"

    id: Mapped[intpk]
    name: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str]
    is_done: Mapped[bool] = mapped_column(nullable=False, default=False)
    added_at: Mapped[added_at]
    done_at: Mapped[datetime.datetime] = mapped_column(nullable=True)
    assignees = relationship(
        "User",
        back_populates="tasks",
        uselist=True,
        secondary="user_task",
    )
    assigner_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=True)
    color: Mapped[str]
    duration: Mapped[datetime.datetime]
    difficulty: Mapped[Difficulty] = mapped_column(nullable=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("project.id"))
    project = relationship("Project", uselist=False, back_populates="tasks")


class UserTask(Base):
    __tablename__ = "user_task"

    id: Mapped[intpk]
    github_data: Mapped[dict] = mapped_column(JSON, nullable=True)
    task_id: Mapped[int] = mapped_column(ForeignKey("task.id"), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    is_employee: Mapped[bool] = mapped_column(nullable=False, default=True)
