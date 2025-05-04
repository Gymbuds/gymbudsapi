"""candidates

Revision ID: 903874a93347
Revises: 5a913a3a0547
Create Date: 2025-05-03 18:07:58.382194

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '903874a93347'
down_revision: Union[str, None] = '5a913a3a0547'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table("match_candidates",sa.Column("id",sa.Integer(),primary_key=True),
                    sa.Column("user_id",sa.Integer(),nullable=False),
                    sa.Column("candidate_user_id",sa.Integer(),nullable=False),
                    sa.Column("status",sa.Enum('ACCEPTED', 'REJECTED', 'PENDING',name='status'), nullable=False),
                    sa.Column("score",sa.Integer(),nullable=False),
                    sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
                    sa.ForeignKeyConstraint(["candidate_user_id"], ["users.id"], ondelete="CASCADE"),
                    sa.UniqueConstraint("user_id", "candidate_user_id", name="candidate_user_pair")
                    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("match_candidates")
    op.execute("DROP type status")

