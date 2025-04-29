"""zip+user_goals

Revision ID: 5a913a3a0547
Revises: 0756a986a942
Create Date: 2025-04-28 22:16:02.744761

"""
from typing import Sequence, Union
from app.db.models.user_goal import GymGoal 
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5a913a3a0547'
down_revision: Union[str, None] = '0756a986a942'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.drop_column("users","preferred_workout_goals")
    op.add_column("users", sa.Column("zip_code", sa.String(), nullable=True))
    op.create_table(
        'user_goals',
        sa.Column('id', sa.Integer(), primary_key=True, index=True),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
        sa.Column('goal', sa.Enum(GymGoal, name="gymgoal"), nullable=False),
    ) 


def downgrade() -> None:
    """Downgrade schema."""
    op.add_column('users', sa.Column('preferred_workout_goals', sa.Text(), nullable=True))
    op.drop_column('users','zip_code')
    op.drop_table('user_goals')
    op.execute('DROP TYPE gymgoal')
