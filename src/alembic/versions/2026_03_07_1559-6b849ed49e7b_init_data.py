"""init_data

Revision ID: 6b849ed49e7b
Revises:
Create Date: 2026-03-07 15:59:49.224701

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6b849ed49e7b'
down_revision: Union[str, Sequence[str], None] = None
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
    op.create_index(op.f('ix_calls_day_of_week'), 'calls', ['day_of_week'], unique=False)
    op.create_index(op.f('ix_calls_end_time'), 'calls', ['end_time'], unique=False)
    op.create_index(op.f('ix_calls_lesson_number'), 'calls', ['lesson_number'], unique=False)
    op.create_index(op.f('ix_calls_start_time'), 'calls', ['start_time'], unique=False)
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
    op.create_index(op.f('ix_schedule_class_number'), 'schedule', ['class_number'], unique=False)
    op.create_index(op.f('ix_schedule_class_parallel'), 'schedule', ['class_parallel'], unique=False)
    op.create_index(op.f('ix_schedule_day_of_week'), 'schedule', ['day_of_week'], unique=False)
    op.create_index(op.f('ix_schedule_room'), 'schedule', ['room'], unique=False)
    op.create_index(op.f('ix_schedule_subject'), 'schedule', ['subject'], unique=False)
    op.create_table('users',
    sa.Column('uuid', sa.Uuid(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('name', sa.String(length=50), nullable=True, comment='Имя пользователя'),
    sa.Column('role', sa.String(length=50), nullable=False, comment='Роль пользователя'),
    sa.Column('status', sa.String(length=10), nullable=False, comment='Статус пользователя'),
    sa.Column('last_activity_at', sa.DateTime(), nullable=True, comment='Дата и время последней активности пользователя'),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.PrimaryKeyConstraint('uuid', name=op.f('pk_users'))
    )
    op.create_index(op.f('ix_users_last_activity_at'), 'users', ['last_activity_at'], unique=False)
    op.create_index(op.f('ix_users_name'), 'users', ['name'], unique=False)
    op.create_index(op.f('ix_users_role'), 'users', ['role'], unique=False)
    op.create_index(op.f('ix_users_status'), 'users', ['status'], unique=False)
    op.create_index(op.f('ix_users_user_id'), 'users', ['user_id'], unique=True)
    op.create_table('students',
    sa.Column('uuid', sa.Uuid(), server_default=sa.text('gen_random_uuid()'), nullable=False, comment='Unique UUID'),
    sa.Column('user_uuid', sa.Uuid(), nullable=True),
    sa.Column('first_name', sa.String(length=50), nullable=True, comment='Фамилия'),
    sa.Column('last_name', sa.String(length=50), nullable=True, comment='Имя'),
    sa.Column('second_name', sa.String(length=50), nullable=True, comment='Отчество'),
    sa.Column('birth_day', sa.Date(), nullable=True, comment='Дата рождения'),
    sa.Column('class_number', sa.Integer(), nullable=True, comment='Номер класса'),
    sa.Column('class_parallel', sa.String(length=1), nullable=True, comment='Параллель'),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.ForeignKeyConstraint(['user_uuid'], ['users.uuid'], name=op.f('fk_students_user_uuid_users')),
    sa.PrimaryKeyConstraint('uuid', name=op.f('pk_students')),
    sa.UniqueConstraint('user_uuid', name=op.f('uq_students_user_uuid'))
    )
    op.create_index(op.f('ix_students_birth_day'), 'students', ['birth_day'], unique=False)
    op.create_index(op.f('ix_students_class_parallel'), 'students', ['class_parallel'], unique=False)
    op.create_index(op.f('ix_students_first_name'), 'students', ['first_name'], unique=False)
    op.create_index(op.f('ix_students_last_name'), 'students', ['last_name'], unique=False)
    op.create_index(op.f('ix_students_second_name'), 'students', ['second_name'], unique=False)
    op.create_table('teachers',
    sa.Column('uuid', sa.Uuid(), server_default=sa.text('gen_random_uuid()'), nullable=False, comment='Unique UUID'),
    sa.Column('user_uuid', sa.Uuid(), nullable=True),
    sa.Column('first_name', sa.String(length=50), nullable=True, comment='Фамилия'),
    sa.Column('last_name', sa.String(length=50), nullable=True, comment='Имя'),
    sa.Column('second_name', sa.String(length=50), nullable=True, comment='Отчество'),
    sa.Column('birth_day', sa.Date(), nullable=True, comment='Дата рождения'),
    sa.Column('employment_date', sa.Date(), nullable=True, comment='Дата трудоустройства'),
    sa.Column('total_years_at_hire', sa.Integer(), nullable=True, comment='Общий стаж (лет) на дату приема'),
    sa.Column('total_months_at_hire', sa.Integer(), nullable=True, comment='Общий стаж (месяцев) на дату приема'),
    sa.Column('total_days_at_hire', sa.Integer(), nullable=True, comment='Общий стаж (дней) на дату приема'),
    sa.Column('teacher_years_at_hire', sa.Integer(), nullable=True, comment='Педагогический стаж (лет) на дату приема'),
    sa.Column('teacher_months_at_hire', sa.Integer(), nullable=True, comment='Педагогический стаж (месяцев) на дату приема'),
    sa.Column('teacher_days_at_hire', sa.Integer(), nullable=True, comment='Педагогический стаж (дней) на дату приема'),
    sa.Column('education', sa.String(length=50), nullable=True, comment='Образование'),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.ForeignKeyConstraint(['user_uuid'], ['users.uuid'], name=op.f('fk_teachers_user_uuid_users')),
    sa.PrimaryKeyConstraint('uuid', name=op.f('pk_teachers')),
    sa.UniqueConstraint('user_uuid', name=op.f('uq_teachers_user_uuid'))
    )
    op.create_index(op.f('ix_teachers_birth_day'), 'teachers', ['birth_day'], unique=False)
    op.create_index(op.f('ix_teachers_education'), 'teachers', ['education'], unique=False)
    op.create_index(op.f('ix_teachers_employment_date'), 'teachers', ['employment_date'], unique=False)
    op.create_index(op.f('ix_teachers_first_name'), 'teachers', ['first_name'], unique=False)
    op.create_index(op.f('ix_teachers_last_name'), 'teachers', ['last_name'], unique=False)
    op.create_index(op.f('ix_teachers_second_name'), 'teachers', ['second_name'], unique=False)
    op.create_index(op.f('ix_teachers_teacher_days_at_hire'), 'teachers', ['teacher_days_at_hire'], unique=False)
    op.create_index(op.f('ix_teachers_teacher_months_at_hire'), 'teachers', ['teacher_months_at_hire'], unique=False)
    op.create_index(op.f('ix_teachers_teacher_years_at_hire'), 'teachers', ['teacher_years_at_hire'], unique=False)
    op.create_index(op.f('ix_teachers_total_days_at_hire'), 'teachers', ['total_days_at_hire'], unique=False)
    op.create_index(op.f('ix_teachers_total_months_at_hire'), 'teachers', ['total_months_at_hire'], unique=False)
    op.create_index(op.f('ix_teachers_total_years_at_hire'), 'teachers', ['total_years_at_hire'], unique=False)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f('ix_teachers_total_years_at_hire'), table_name='teachers')
    op.drop_index(op.f('ix_teachers_total_months_at_hire'), table_name='teachers')
    op.drop_index(op.f('ix_teachers_total_days_at_hire'), table_name='teachers')
    op.drop_index(op.f('ix_teachers_teacher_years_at_hire'), table_name='teachers')
    op.drop_index(op.f('ix_teachers_teacher_months_at_hire'), table_name='teachers')
    op.drop_index(op.f('ix_teachers_teacher_days_at_hire'), table_name='teachers')
    op.drop_index(op.f('ix_teachers_second_name'), table_name='teachers')
    op.drop_index(op.f('ix_teachers_last_name'), table_name='teachers')
    op.drop_index(op.f('ix_teachers_first_name'), table_name='teachers')
    op.drop_index(op.f('ix_teachers_employment_date'), table_name='teachers')
    op.drop_index(op.f('ix_teachers_education'), table_name='teachers')
    op.drop_index(op.f('ix_teachers_birth_day'), table_name='teachers')
    op.drop_table('teachers')
    op.drop_index(op.f('ix_students_second_name'), table_name='students')
    op.drop_index(op.f('ix_students_last_name'), table_name='students')
    op.drop_index(op.f('ix_students_first_name'), table_name='students')
    op.drop_index(op.f('ix_students_class_parallel'), table_name='students')
    op.drop_index(op.f('ix_students_birth_day'), table_name='students')
    op.drop_table('students')
    op.drop_index(op.f('ix_users_user_id'), table_name='users')
    op.drop_index(op.f('ix_users_status'), table_name='users')
    op.drop_index(op.f('ix_users_role'), table_name='users')
    op.drop_index(op.f('ix_users_name'), table_name='users')
    op.drop_index(op.f('ix_users_last_activity_at'), table_name='users')
    op.drop_table('users')
    op.drop_index(op.f('ix_schedule_subject'), table_name='schedule')
    op.drop_index(op.f('ix_schedule_room'), table_name='schedule')
    op.drop_index(op.f('ix_schedule_day_of_week'), table_name='schedule')
    op.drop_index(op.f('ix_schedule_class_parallel'), table_name='schedule')
    op.drop_index(op.f('ix_schedule_class_number'), table_name='schedule')
    op.drop_table('schedule')
    op.drop_index(op.f('ix_calls_start_time'), table_name='calls')
    op.drop_index(op.f('ix_calls_lesson_number'), table_name='calls')
    op.drop_index(op.f('ix_calls_end_time'), table_name='calls')
    op.drop_index(op.f('ix_calls_day_of_week'), table_name='calls')
    op.drop_table('calls')
