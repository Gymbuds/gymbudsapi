"""add nullable to workout dates

Revision ID: 11c7bbb21988
Revises: a443023eb0e8
Create Date: 2025-05-18 16:38:08.728116

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '11c7bbb21988'
down_revision: Union[str, None] = 'a443023eb0e8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.alter_column("ai_advices",sa.Column("workout_earliest_date",sa.DateTime(),nullable=True))
    op.alter_column("ai_advices",sa.Column("workout_latest_date",sa.DateTime(),nullable=True))



def downgrade() -> None:
    """Downgrade schema."""
    op.alter_column("ai_advices",sa.Column("workout_earliest_date",sa.DateTime(),nullable=False))
    op.alter_column("ai_advices",sa.Column("workout_latest_date",sa.DateTime(),nullable=False))
