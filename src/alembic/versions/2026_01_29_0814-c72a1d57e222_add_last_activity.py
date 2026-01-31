"""add_last_activity

Revision ID: c72a1d57e222
Revises: 4e9c1e2d7248
Create Date: 2026-01-29 08:14:05.636720

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c72a1d57e222'
down_revision: Union[str, Sequence[str], None] = '4e9c1e2d7248'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('users', sa.Column('last_activity_at', sa.DateTime(), nullable=True))



def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('users', 'last_activity_at')
