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

# revision identifiers, used by Alembic.
revision: str = "54b56d6aec6d"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


OPERATION_TYPE = pg.ENUM(OperationType, name="operation_type")


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "users",
        sa.Column("id", sa.Uuid, primary_key=True),
        sa.Column("chat_id", sa.Integer, nullable=False, unique=True),
    )
    op.create_index("idx_users_chat_id", "users", ["chat_id"])

    op.create_table(
        "operations",
        sa.Column("operation_id", sa.Uuid, primary_key=True),
        sa.Column("user_id", sa.Uuid, sa.ForeignKey("users.id"), nullable=False),
        sa.Column(
            "op_type",
            OPERATION_TYPE,
            nullable=False,
        ),
        sa.Column("took", sa.Double(), nullable=True),
        sa.Column("details", pg.JSONB, nullable=False, server_default="{}"),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("operations")
    OPERATION_TYPE.drop(op.get_bind(), checkfirst=True)
    op.drop_table("users")
