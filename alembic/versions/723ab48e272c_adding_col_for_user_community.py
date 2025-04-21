"""adding col for user community

Revision ID: 723ab48e272c
Revises: a2bac0746e8e
Create Date: 2025-04-21 00:15:39.563905

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '723ab48e272c'
down_revision: Union[str, None] = 'a2bac0746e8e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        'user_communities',
        sa.Column(
            'is_preferred_gym',
            sa.Boolean(),
            nullable=False,
            server_default=sa.text('false')  
        )
    )
    op.alter_column('user_communities', 'is_preferred_gym', server_default=None)
def downgrade() -> None:
    """downgrade"""
    op.drop_column("user_communities",'is_preferred_gym')
