"""update user_uuid

Revision ID: 139609e2cd68
Revises: 4b246f57ce6c
Create Date: 2026-02-17 11:50:00.246716

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '139609e2cd68'
down_revision: Union[str, Sequence[str], None] = '4b246f57ce6c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    # Удаляем существующие внешние ключи (если они есть)
    op.drop_constraint('fk_students_user_uuid_users', 'students', type_='foreignkey', if_exists=True)
    op.drop_constraint('fk_teachers_user_uuid_users', 'teachers', type_='foreignkey', if_exists=True)

    # Изменяем тип колонки в students с явным преобразованием
    op.alter_column('students', 'user_uuid',
               type_=sa.Uuid(),
               existing_type=sa.BIGINT(),
               existing_nullable=True,
               postgresql_using='user_uuid::text::uuid')

    # Изменяем тип колонки в teachers с явным преобразованием
    op.alter_column('teachers', 'user_uuid',
               type_=sa.Uuid(),
               existing_type=sa.BIGINT(),
               existing_nullable=True,
               postgresql_using='user_uuid::text::uuid')

    # Создаем новые внешние ключи
    op.create_foreign_key(op.f('fk_students_user_uuid_users'),
                         'students', 'users',
                         ['user_uuid'], ['uuid'])
    op.create_foreign_key(op.f('fk_teachers_user_uuid_users'),
                         'teachers', 'users',
                         ['user_uuid'], ['uuid'])


def downgrade() -> None:
    """Downgrade schema."""
    # Удаляем внешние ключи
    op.drop_constraint(op.f('fk_teachers_user_uuid_users'),
                      'teachers', type_='foreignkey')
    op.drop_constraint(op.f('fk_students_user_uuid_users'),
                      'students', type_='foreignkey')

    # Возвращаем тип обратно к BIGINT с явным преобразованием
    op.alter_column('teachers', 'user_uuid',
               existing_type=sa.Uuid(),
               type_=sa.BIGINT(),
               existing_nullable=True,
               postgresql_using='user_uuid::text::bigint')

    op.alter_column('students', 'user_uuid',
               existing_type=sa.Uuid(),
               type_=sa.BIGINT(),
               existing_nullable=True,
               postgresql_using='user_uuid::text::bigint')

    # Восстанавливаем внешние ключи если нужно
    # op.create_foreign_key(...)