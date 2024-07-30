from sqlalchemy.orm import Mapped, relationship

from database import Base
from my_type_notation import intpk


class Organization(Base):
    __tablename__ = "organization"

    id: Mapped[intpk]
    name: Mapped[str]
    description: Mapped[str]
    staff = relationship("User", uselist=True, back_populates="organization")
    projects = relationship("Project", uselist=True, back_populates="organization")
