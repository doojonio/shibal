"""initial_migration

Revision ID: 54b56d6aec6d
Revises:
Create Date: 2025-03-07 07:14:28.028052

"""

from typing import Sequence, Union

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql as pg

from alembic import op
from app.models.operations import OperationType
from app.models.orders import OrderType

# revision identifiers, used by Alembic.
revision: str = "54b56d6aec6d"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


OPERATION_TYPE = pg.ENUM(OperationType, name="operation_type")
ORDER_TYPE = pg.ENUM(OrderType, name="order_type")


def upgrade() -> None:
    """Upgrade schema."""
    op.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp"')

    op.create_table(
        "users",
        sa.Column(
            "id",
            sa.Uuid,
            primary_key=True,
            server_default=sa.text("uuid_generate_v4()"),
        ),
        sa.Column("chat_id", sa.Integer, nullable=False, unique=True),
        sa.Column("op_balance", sa.Integer, nullable=False, server_default="0"),
        sa.Column(
            "created", sa.DateTime, nullable=False, server_default=sa.text("now()")
        ),
    )
    op.create_index("idx_users_chat_id", "users", ["chat_id"])

    op.create_table(
        "operations",
        sa.Column(
            "id",
            sa.Uuid,
            primary_key=True,
            server_default=sa.text("uuid_generate_v4()"),
        ),
        sa.Column("user_id", sa.Uuid, sa.ForeignKey("users.id"), nullable=False),
        sa.Column(
            "op_type",
            OPERATION_TYPE,
            nullable=False,
        ),
        sa.Column("details", pg.JSONB, nullable=False, server_default="{}"),
        sa.Column(
            "started", sa.DateTime, nullable=False, server_default=sa.text("now()")
        ),
        sa.Column("took", sa.Double(), nullable=True),
    )
    op.create_index("idx_operations_user_id", "operations", ["user_id"])

    op.create_table(
        "orders",
        sa.Column(
            "id",
            sa.Uuid,
            primary_key=True,
            server_default=sa.text("uuid_generate_v4()"),
        ),
        sa.Column("user_id", sa.Uuid, sa.ForeignKey("users.id"), nullable=False),
        sa.Column("order_type", ORDER_TYPE, nullable=False),
        sa.Column("op_added", sa.Integer, nullable=False),
        sa.Column(
            "created", sa.DateTime, nullable=False, server_default=sa.text("now()")
        ),
        sa.Column("payed", sa.DateTime, nullable=True),
    )
    op.create_index("idx_orders_user_id", "orders", ["user_id"])


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("orders")
    ORDER_TYPE.drop(op.get_bind())
    op.drop_table("operations")
    OPERATION_TYPE.drop(op.get_bind())
    op.drop_table("users")
