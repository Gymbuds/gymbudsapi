"""chat model message model

Revision ID: 2d8449f790e3
Revises: 7c392146f16d
Create Date: 2025-05-06 22:00:03.205142

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2d8449f790e3'
down_revision: Union[str, None] = '7c392146f16d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table("chats",
                    sa.Column("id",sa.Integer(),nullable=False,primary_key=True,index=True),
                    sa.Column("created_at",sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
                    sa.Column("user_id1", sa.Integer(), nullable=False),
                    sa.Column("user_id2", sa.Integer(), nullable=False),
                    sa.ForeignKeyConstraint(["user_id1"], ["users.id"], ondelete="CASCADE"),
                    sa.ForeignKeyConstraint(["user_id2"], ["users.id"], ondelete="CASCADE"),
                    sa.UniqueConstraint("user_id1", "user_id2", name="chat_user_pair")
                    )
    op.create_table("messages",
                    sa.Column("id",sa.Integer(),nullable=False,primary_key=True,index=True),
                    sa.Column("chat_id",sa.Integer()),
                    sa.Column("sender_id",sa.Integer()),
                    sa.Column("content",sa.String()),
                    sa.Column("timestamp",sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
                    sa.ForeignKeyConstraint(["chat_id"],["chats.id"],ondelete="CASCADE"),
                    sa.ForeignKeyConstraint(["sender_id"],["users.id"],ondelete="CASCADE")
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("messages")
    op.drop_table("chats")
