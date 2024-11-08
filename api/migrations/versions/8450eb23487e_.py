"""empty message

Revision ID: 8450eb23487e
Revises: 66642bc11750
Create Date: 2024-08-07 15:20:58.315979

"""

from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "8450eb23487e"
down_revision: Union[str, None] = "66642bc11750"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(
        "user_task_task_id_fkey", "user_task", type_="foreignkey"
    )
    op.create_foreign_key(
        None, "user_task", "task", ["task_id"], ["id"], ondelete="CASCADE"
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, "user_task", type_="foreignkey")
    op.create_foreign_key(
        "user_task_task_id_fkey", "user_task", "task", ["task_id"], ["id"]
    )
    # ### end Alembic commands ###
