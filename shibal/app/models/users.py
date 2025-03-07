from uuid import UUID

from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .operations import Operation


class User(Base):
    __tablename__ = "users"

    id: Mapped[UUID] = mapped_column(primary_key=True)
    chat_id: Mapped[int] = mapped_column()

    operations: Mapped[list["Operation"]] = relationship(back_populates="user")
