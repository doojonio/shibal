from sqlalchemy import select

from app.db import AsyncSession
from app.models.users import User


async def get_or_create_user_by_chat(db: AsyncSession, chat_id: int) -> User:
    result = await db.execute(select(User).filter_by(chat_id=chat_id).limit(1))

    if user := result.scalar():
        return user

    user = User(chat_id=chat_id)
    db.add(user)
    await db.commit()

    return user
