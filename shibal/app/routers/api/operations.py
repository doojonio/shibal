from typing import Iterable

from fastapi import APIRouter, Depends
from sqlalchemy import select

from app.db import AsyncSession, get_async_db
from app.models.operations import Operation
from app.schemas.operations import OperationScheme

router = APIRouter(prefix="/operations", tags=["operations"])


@router.get("/list", response_model=list[OperationScheme])
async def list_operations(
    db: AsyncSession = Depends(get_async_db),
) -> Iterable[Operation]:
    operations = await db.execute(select(Operation).order_by(Operation.started.desc()))

    return operations.scalars()
