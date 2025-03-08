from datetime import date, timedelta
from typing import Iterable
from uuid import UUID

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy import func, literal_column, select

from app.db import AsyncSession, get_async_db
from app.models.users import User
from app.schemas.common import ErrorScheme
from app.schemas.users import UserScheme

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/list", response_model=list[UserScheme])
async def list_users(db: AsyncSession = Depends(get_async_db)) -> Iterable[User]:
    users = await db.execute(select(User).order_by(User.id.desc()))

    return users.scalars()


@router.get("/get", response_model=UserScheme)
async def get_user(
    user_id: UUID, db: AsyncSession = Depends(get_async_db)
) -> User | None:
    user = await db.execute(select(User).filter_by(id=user_id).order_by(User.id.desc()))

    return user.scalar()


@router.get("/count_per_day", responses={200: {}, 403: {"model": ErrorScheme}})
async def get_users_count_per_day(
    days: int,
    db: AsyncSession = Depends(get_async_db),
):
    if days > 100:
        return JSONResponse({"error": "Can't load more than 100 days"}, status_code=403)

    after = date.today() - timedelta(days=days)

    counts = await db.execute(
        select(
            func.date_trunc("day", User.created).label("day"),
            func.count("*").label("count"),
        )
        .filter(User.created >= after)
        .group_by(literal_column("day"))
        .order_by(literal_column("day").desc())
    )

    return {c[0]: c[1] for c in counts}
