"""empty message

Revision ID: cdc369cb5e36
Revises: 9338949fdaa3
Create Date: 2024-07-24 19:00:14.127427

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'cdc369cb5e36'
down_revision: Union[str, None] = '9338949fdaa3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'hashed_password')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('hashed_password', sa.VARCHAR(length=1024), autoincrement=False, nullable=True))
    # ### end Alembic commands ###
