from contextlib import asynccontextmanager
from datetime import datetime

from app.db import AsyncSession
from app.models.operations import Operation, OperationTypes
from app.models.users import User

from time import time


@asynccontextmanager
async def new_operation(db: AsyncSession, user: User, op_type: OperationTypes):
    new_op = Operation(user=user, op_type=op_type, started=datetime.now())
    db.add(new_op)

    started_at = time()
    try:
        yield new_op
    finally:
        elapsed = time() - started_at
        new_op.took = elapsed
        user.op_balance -= 1

        await db.flush()
