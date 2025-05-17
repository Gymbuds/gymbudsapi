"""timestamp

Revision ID: a443023eb0e8
Revises: bc690f305cf7
Create Date: 2025-05-16 15:25:50.460676

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'a443023eb0e8'
down_revision: Union[str, None] = 'bc690f305cf7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Ensure the column is timezone-aware and has a server default
    op.execute("""
        ALTER TABLE workout_logs 
        ALTER COLUMN date TYPE TIMESTAMP WITH TIME ZONE 
        USING date AT TIME ZONE 'UTC'
    """)
    
    op.alter_column(
        'workout_logs',
        'date',
        existing_type=sa.DateTime(timezone=True),
        server_default=sa.func.now()
    )

def downgrade() -> None:
    op.alter_column(
        'workout_logs',
        'date',
        existing_type=sa.DateTime(timezone=True),
        server_default=None
    )
