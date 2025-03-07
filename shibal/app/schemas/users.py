from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class UserScheme(BaseModel):
    id: UUID
    chat_id: int
    op_balance: int
    created: datetime

    class Config:
        orm_mode = True
