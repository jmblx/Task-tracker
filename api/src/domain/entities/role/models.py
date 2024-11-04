from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.db.database import Base
from core.db.db_types import intpk
from domain.entities.user.models import User


class Role(Base):
    __tablename__ = "role"

    id: Mapped[intpk]
    name: Mapped[str] = mapped_column(nullable=False)
    permissions: Mapped[dict] = mapped_column(JSON)
    users: Mapped[list["User"]] = relationship(
        back_populates="role", uselist=True
    )
