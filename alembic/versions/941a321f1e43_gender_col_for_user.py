"""gender col for user

Revision ID: 941a321f1e43
Revises: 723ab48e272c
Create Date: 2025-04-23 19:12:11.037746

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '941a321f1e43'
down_revision: Union[str, None] = '723ab48e272c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("users",sa.Column("gender",sa.String()))
    


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("users","gender")
