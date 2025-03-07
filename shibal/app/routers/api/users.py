from typing import Iterable

from fastapi import APIRouter, Depends
from sqlalchemy import select

from app.db import AsyncSession, get_async_db
from app.models.users import User
from app.schemas.users import UserScheme

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/list", response_model=list[UserScheme])
async def list_users(db: AsyncSession = Depends(get_async_db)) -> Iterable[User]:
    users = await db.execute(select(User).order_by(User.id.desc()))

    return users.scalars()
