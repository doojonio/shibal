from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from app.models.operations import OperationTypes


class OperationScheme(BaseModel):
    id: UUID
    user_id: UUID
    op_type: OperationTypes
    details: dict[str, int | str | bool]
    started: datetime
    took: float | None

    class Config:
        orm_mode = True
