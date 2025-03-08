from datetime import datetime
from typing import Iterable
from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy import func, select, text

from app.db import AsyncSession, get_async_db
from app.models.operations import Operation, OperationTypes
from app.schemas.operations import OperationScheme

router = APIRouter(prefix="/operations", tags=["operations"])


@router.get("/list", response_model=list[OperationScheme])
async def list_operations(
    db: AsyncSession = Depends(get_async_db),
    user_id: UUID | None = None,
) -> Iterable[Operation]:
    stmt = select(Operation).order_by(Operation.started.desc())

    if user_id is not None:
        stmt = stmt.filter_by(user_id=user_id)

    operations = await db.execute(stmt)

    return operations.scalars()


@router.get("/count_per_hour")
async def get_operations_count_per_hour(
    db: AsyncSession = Depends(get_async_db),
    user_id: UUID | None = None,
) -> list[tuple[datetime, int]]:
    stmt = (
        select(
            func.date_trunc("hour", Operation.started).label("hour"),
            func.count("*").label("count"),
        )
        .filter(Operation.started >= func.now().op("-")(text("INTERVAL '5 hours'")))
        .group_by(text("hour"))
    )

    if user_id is not None:
        stmt = stmt.filter(Operation.user_id == user_id)

    counts = await db.execute(stmt)

    return list(counts.tuples())


@router.get("/count_per_type")
async def get_operations_count_per_type(
    db: AsyncSession = Depends(get_async_db),
    user_id: UUID | None = None,
) -> list[tuple[OperationTypes, int]]:
    stmt = (
        select(
            Operation.op_type.label("type"),
            func.count("*").label("count"),
        )
        .group_by(Operation.op_type)
        .order_by(Operation.op_type)
    )

    if user_id is not None:
        stmt = stmt.filter(Operation.user_id == user_id)

    counts = await db.execute(stmt)

    return list(counts.tuples())
