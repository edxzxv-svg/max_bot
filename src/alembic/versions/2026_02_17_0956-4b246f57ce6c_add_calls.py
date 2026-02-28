"""add_calls

Revision ID: 4b246f57ce6c
Revises: 03944b5456b1
Create Date: 2026-02-17 09:56:27.752048

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '4b246f57ce6c'
down_revision: Union[str, Sequence[str], None] = '03944b5456b1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('calls',
    sa.Column('uuid', sa.Uuid(), nullable=False),
    sa.Column('day_of_week', sa.Integer(), nullable=False, comment='День недели'),
    sa.Column('lesson_number', sa.Integer(), nullable=False, comment='Номер урока'),
    sa.Column('start_time', sa.Time(), nullable=False, comment='Время начала урока'),
    sa.Column('end_time', sa.Time(), nullable=False, comment='Время окончания урока'),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.PrimaryKeyConstraint('uuid', name=op.f('pk_calls'))
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('calls')

