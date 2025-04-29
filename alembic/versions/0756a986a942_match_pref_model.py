"""match-pref-model

Revision ID: 0756a986a942
Revises: 738401a3f23b
Create Date: 2025-04-28 20:35:39.803641

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0756a986a942'
down_revision: Union[str, None] = '738401a3f23b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table("match_preferences",
                    sa.Column('id', sa.Integer(), primary_key=True, nullable=False),
                    sa.Column('user_id',sa.Integer(),nullable=False),
                    sa.Column('gender',sa.Enum('MALE', 'FEMALE', 'BOTH',name='gender'), nullable=False),
                    sa.Column('start_weight',sa.Integer(),nullable = False),
                    sa.Column('end_weight',sa.Integer(),nullable=False),
                    sa.Column('max_location_distance_miles',nullable=False),
                    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'))


def downgrade() -> None:
    """Downgrade schema."""
    
    op.drop_table("match_preferences")
    op.execute('DROP TYPE gender') 