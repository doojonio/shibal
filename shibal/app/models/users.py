import datetime
from uuid import UUID

from sqlalchemy import text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .operations import Operation
from .orders import Order


class User(Base):
    __tablename__ = "users"

    id: Mapped[UUID] = mapped_column(
        primary_key=True, server_default=text("uuid_generate_v4()")
    )
    chat_id: Mapped[int] = mapped_column()
    op_balance: Mapped[int] = mapped_column(default=0)
    created: Mapped[datetime.datetime] = mapped_column(server_default=text("now()"))

    operations: Mapped[list["Operation"]] = relationship(back_populates="user")
    orders: Mapped[list["Order"]] = relationship(back_populates="user")
