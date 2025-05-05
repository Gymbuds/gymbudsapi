"""age column match pref

Revision ID: 7c392146f16d
Revises: 903874a93347
Create Date: 2025-05-04 18:34:31.513289

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7c392146f16d'
down_revision: Union[str, None] = '903874a93347'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("match_preferences",sa.Column("start_age",sa.Integer(),nullable=True))
    op.add_column("match_preferences",sa.Column("end_age",sa.Integer(),nullable=True))

    op.execute("UPDATE match_preferences SET start_age = 18")
    op.execute("UPDATE match_preferences SET end_age = 100")
    op.alter_column("match_preferences","start_age",nullable=False)
    op.alter_column("match_preferences","end_age",nullable=False)

def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("match_preferences","age")
