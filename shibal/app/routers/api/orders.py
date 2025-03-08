from datetime import date, timedelta
from typing import Iterable

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy import func, literal_column, select

from app.db import AsyncSession, get_async_db
from app.models.orders import Order
from app.schemas.common import ErrorScheme
from app.schemas.orders import OrderScheme

router = APIRouter(prefix="/orders", tags=["orders"])


@router.get("/list", response_model=list[OrderScheme])
async def list_orders(db: AsyncSession = Depends(get_async_db)) -> Iterable[Order]:
    orders = await db.execute(select(Order).order_by(Order.created.desc()))

    return orders.scalars()


@router.get("/count_per_day", responses={200: {}, 403: {"model": ErrorScheme}})
async def get_orders_count_per_day(
    days: int,
    db: AsyncSession = Depends(get_async_db),
):
    if days > 100:
        return JSONResponse({"error": "Can't load more than 100 days"}, status_code=403)

    after = date.today() - timedelta(days=days)

    counts = await db.execute(
        select(
            func.date_trunc("day", Order.created).label("day"),
            func.count("*").label("count"),
        )
        .filter(Order.created >= after)
        .group_by(literal_column("day"))
        .order_by(literal_column("day").desc())
    )

    return {c[0]: c[1] for c in counts}
