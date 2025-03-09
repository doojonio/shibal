import pytest

from tests import factories as f

URL = "/api/v1/users/list"


@pytest.mark.asyncio()
async def test_if_has_users(db, client):
    user = f.UserFactory.build()
    db.add(user)
    await db.flush()

    assert (await client.get(URL)).json() == [
        {
            "id": str(user.id),
            "chat_id": user.chat_id,
            "op_balance": user.op_balance,
            "created": user.created.isoformat(),
        }
    ]
