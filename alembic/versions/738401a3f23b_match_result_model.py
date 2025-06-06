"""match result model

Revision ID: 738401a3f23b
Revises: 941a321f1e43
Create Date: 2025-04-23 21:59:37.642878

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '738401a3f23b'
down_revision: Union[str, None] = '941a321f1e43'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "match_results",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id1", sa.Integer(), nullable=False),
        sa.Column("user_id2", sa.Integer(), nullable=False),
        sa.Column("matched_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(["user_id1"], ["users.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["user_id2"], ["users.id"], ondelete="CASCADE"),
        sa.UniqueConstraint("user_id1", "user_id2", name="uq_user_pair")
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("match_results")
    # ### end Alembic commands ###
