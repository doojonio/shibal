from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from app.models.orders import OrderTypes


class OrderScheme(BaseModel):
    id: UUID
    user_id: UUID
    order_type: OrderTypes
    op_added: int
    created: datetime
    payed: datetime | None

    class Config:
        orm_mode = True
