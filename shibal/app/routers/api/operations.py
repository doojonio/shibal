from datetime import date, datetime, timedelta
from uuid import UUID

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy import Double, cast, func, literal_column, select, text

from app.db import AsyncSession, get_async_db
from app.models.operations import Operation, OperationTypes
from app.schemas.common import ErrorScheme
from app.schemas.operations import OperationScheme

router = APIRouter(prefix="/operations", tags=["operations"])


@router.get(
    "/list",
    responses={200: {"model": list[OperationScheme]}, 403: {"model": ErrorScheme}},
)
async def list_operations(
    db: AsyncSession = Depends(get_async_db),
    user_id: UUID | None = None,
    limit: int = 100,
    page: int = 0,
):
    if limit >= 500:
        return JSONResponse(
            {"error": "Can't load more than 500 records"}, status_code=403
        )

    stmt = select(Operation).order_by(Operation.started.desc()).offset(page * limit)

    if user_id is not None:
        stmt = stmt.filter_by(user_id=user_id)

    operations = await db.execute(stmt)

    return list(operations.scalars())


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


@router.get(
    "/total_cutted_per_day",
    responses={200: {"model": list[tuple[date, int]]}, 403: {"model": ErrorScheme}},
)
async def get_total_cutted_per_day(
    db: AsyncSession = Depends(get_async_db),
    days: int = 5,
    user_id: UUID | None = None,
) -> JSONResponse:
    if days > 365:
        return JSONResponse(
            {"error": "Can't load days more than a 365"}, status_code=403
        )

    after = date.today() - timedelta(days=days)
    stmt = (
        select(
            func.date_trunc("day", Operation.started).label("day"),
            (
                func.sum(cast(Operation.details["length"], Double))
                .op("-")(func.sum(cast(Operation.details["new_length"], Double)))
                .label("cutted")
            ),
        )
        .filter(
            Operation.took.is_not(None),
            Operation.op_type.in_((OperationTypes.CUT, OperationTypes.TRIM)),
            Operation.started >= after,
        )
        .group_by(literal_column("day"))
        .order_by(literal_column("day"))
    )

    if user_id is not None:
        stmt = stmt.filter(Operation.user_id == user_id)

    counts = await db.execute(stmt)

    return JSONResponse([(str(r.day.date()), r.cutted) for r in counts])
