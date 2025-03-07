import datetime

from sqlalchemy import select

from app.db import AsyncSession
from app.models.orders import Order, OrderTypes
from app.models.users import User

OPS_FOR_NEW_USER = 324


async def get_or_create_user_by_chat(
    db: AsyncSession, chat_id: int, with_for_update: bool = False
) -> User:
    stmt = select(User).filter_by(chat_id=chat_id).limit(1)

    if with_for_update:
        stmt = stmt.with_for_update()

    result = await db.execute(stmt)

    if user := result.scalar():
        return user

    return await create_new_user_by_chat(db, chat_id)


async def create_new_user_by_chat(db: AsyncSession, chat_id: int) -> User:
    user = User(chat_id=chat_id)
    db.add(user)
    await db.flush()

    start_order = Order(
        user=user,
        order_type=OrderTypes.START,
        op_added=OPS_FOR_NEW_USER,
        payed=datetime.datetime.now(),
    )

    user.op_balance += OPS_FOR_NEW_USER

    db.add(start_order)
    db.add(user)

    await db.flush()

    return user
