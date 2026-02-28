"""add_shedule

Revision ID: 03944b5456b1
Revises: c72a1d57e222
Create Date: 2026-02-17 01:44:19.443287

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '03944b5456b1'
down_revision: Union[str, Sequence[str], None] = 'c72a1d57e222'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('schedule',
    sa.Column('uuid', sa.Uuid(), nullable=False),
    sa.Column('class_number', sa.Integer(), nullable=False, comment='Номер класса'),
    sa.Column('class_parallel', sa.String(length=1), nullable=False, comment='Параллель'),
    sa.Column('day_of_week', sa.Integer(), nullable=False, comment='День недели'),
    sa.Column('lesson_number', sa.Integer(), nullable=False, comment='Номер урока'),
    sa.Column('subject', sa.String(), nullable=False, comment='Предмет'),
    sa.Column('room', sa.Integer(), nullable=True, comment='Кабинет'),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),

    sa.PrimaryKeyConstraint('uuid', name=op.f('pk_schedule'))
    )



def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('schedule')

