import datetime
import enum
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy.dialects import postgresql as pg

from sqlalchemy import ForeignKey, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .users import User


class OrderTypes(enum.IntEnum):
    START = 0
    PAY = 1
    PROMO = 2


class Order(Base):
    __tablename__ = "orders"

    id: Mapped[UUID] = mapped_column(
        primary_key=True, server_default=text("uuid_generate_v4()")
    )
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"))
    order_type: Mapped[OrderTypes] = mapped_column(
        pg.ENUM(OrderTypes, name="order_type")
    )
    op_added: Mapped[int] = mapped_column(nullable=False)
    created: Mapped[datetime.datetime] = mapped_column(server_default=text("now()"))
    payed: Mapped[datetime.datetime | None] = mapped_column()

    user: Mapped["User"] = relationship(back_populates="orders")
