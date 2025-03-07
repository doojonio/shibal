from fastapi import APIRouter, Depends
from sqlalchemy import select

from app.db import AsyncSession, get_async_db
from app.models.users import User

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/list")
async def list_users(db: AsyncSession = Depends(get_async_db)):
    users = await db.execute(select(User.id, User.chat_id).order_by(User.id.desc()))

    return list(map(list, users))
