"""empty message

Revision ID: 0f0e4919f05f
Revises: fe6efc6ea19a
Create Date: 2024-04-13 21:36:01.026331

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '0f0e4919f05f'
down_revision: Union[str, None] = 'fe6efc6ea19a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Удаление старой колонки с типом TIMESTAMP
    op.drop_column('task', 'duration')

    # Добавление новой колонки с типом INTERVAL
    op.add_column('task', sa.Column('duration', sa.Interval(), nullable=True))


def downgrade() -> None:
    # Удаление новой колонки с типом INTERVAL
    op.drop_column('task', 'duration')

    # Воссоздание старой колонки с типом TIMESTAMP
    op.add_column('task', sa.Column('duration', sa.TIMESTAMP(), nullable=True))
    # ### end Alembic commands ###
