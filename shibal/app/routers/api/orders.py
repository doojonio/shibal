from datetime import date, timedelta
from uuid import UUID

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy import func, literal_column, select

from app.db import AsyncSession, get_async_db
from app.models.orders import Order
from app.schemas.common import ErrorScheme
from app.schemas.orders import OrderScheme

router = APIRouter(prefix="/orders", tags=["orders"])


@router.get(
    "/list", responses={200: {"model": list[OrderScheme]}, 403: {"model": ErrorScheme}}
)
async def list_orders(
    db: AsyncSession = Depends(get_async_db),
    user_id: UUID | None = None,
    limit: int = 100,
    page: int = 0,
):
    if limit >= 500:
        return JSONResponse(
            {"error": "Can't load more than 500 records"}, status_code=403
        )

    stmt = (
        select(Order).order_by(Order.created.desc()).limit(limit).offset(page * limit)
    )

    if user_id is not None:
        stmt = stmt.filter_by(user_id=user_id)

    orders = await db.execute(stmt)

    return list(orders.scalars())


@router.get("/count_per_day", responses={200: {}, 403: {"model": ErrorScheme}})
async def get_orders_count_per_day(
    days: int,
    db: AsyncSession = Depends(get_async_db),
    user_id: UUID | None = None,
):
    if days > 100:
        return JSONResponse({"error": "Can't load more than 100 days"}, status_code=403)

    after = date.today() - timedelta(days=days)

    stmt = (
        select(
            func.date_trunc("day", Order.created).label("day"),
            func.count("*").label("count"),
        )
        .filter(Order.created >= after)
        .group_by(literal_column("day"))
        .order_by(literal_column("day").desc())
    )
    if user_id is not None:
        stmt = stmt.filter(Order.user_id == user_id)

    counts = await db.execute(stmt)

    return {c[0]: c[1] for c in counts}
