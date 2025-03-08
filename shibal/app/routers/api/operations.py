from datetime import datetime
from typing import Iterable

from fastapi import APIRouter, Depends
from sqlalchemy import func, select, text

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


@router.get("/count_per_hour")
async def get_operations_count_per_hour(
    db: AsyncSession = Depends(get_async_db),
) -> list[tuple[datetime, int]]:
    counts = await db.execute(
        select(
            func.date_trunc("hour", Operation.started).label("hour"),
            func.count("*").label("count"),
        )
        .filter(Operation.started >= func.now().op("-")(text("INTERVAL '5 hours'")))
        .group_by(text("hour"))
    )

    return list(counts.tuples())
