from contextlib import contextmanager
from datetime import datetime
from time import time

from app.db import Session
from app.models.operations import Operation, OperationTypes
from app.models.users import User


@contextmanager
def new_operation(db: Session, user: User, op_type: OperationTypes):
    new_op = Operation(user=user, op_type=op_type, details={}, started=datetime.now())
    db.add(new_op)

    started_at = time()
    try:
        yield new_op
    finally:
        elapsed = time() - started_at
        new_op.took = elapsed
        user.op_balance -= 1

        db.flush()
