from typing import Iterable

from fastapi import APIRouter, Depends
from sqlalchemy import select

from app.db import AsyncSession, get_async_db
from app.models.orders import Order
from app.schemas.orders import OrderScheme

router = APIRouter(prefix="/orders", tags=["orders"])


@router.get("/list", response_model=list[OrderScheme])
async def list_orders(db: AsyncSession = Depends(get_async_db)) -> Iterable[Order]:
    orders = await db.execute(select(Order).order_by(Order.created.desc()))

    return orders.scalars()
