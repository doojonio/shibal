import pytest
from sqlalchemy import select

from app.models.users import User
from tests import factories as f

URL = "/api/v1/users/list"


@pytest.mark.asyncio()
async def test_if_big_limit(db, client):
    user = await f.UserFactory()
    print(user.id)
    print((await db.execute(select(User))).all())
    print((await client.get(URL)).json())
