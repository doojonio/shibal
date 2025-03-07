import datetime
import enum
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import ForeignKey, text
from sqlalchemy.dialects import postgresql as pg
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .users import User


class OperationType(enum.IntEnum):
    TRIM = 0
    CUT = 1
    VOLUME = 2
    FADES = 3


class Operation(Base):
    __tablename__ = "operations"

    id: Mapped[UUID] = mapped_column(
        primary_key=True, server_default=text("uuid_generate_v4()")
    )
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"))
    op_type: Mapped[OperationType] = mapped_column()
    details: Mapped[dict] = mapped_column(pg.JSON, nullable=False)
    started: Mapped[datetime.datetime] = mapped_column(server_default=text("now()"))
    took: Mapped[float | None] = mapped_column(nullable=True)

    user: Mapped["User"] = relationship(back_populates="operations")
