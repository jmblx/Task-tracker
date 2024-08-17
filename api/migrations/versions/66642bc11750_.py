from datetime import datetime
from typing import Sequence, Union
from uuid import uuid4

import sqlalchemy as sa
from alembic import op
from auth.jwt_utils import hash_password
from config import API_ADMIN_PWD
from sqlalchemy import UUID
from sqlalchemy.dialects import postgresql
from sqlalchemy.dialects.postgresql import BYTEA, JSON

# revision identifiers, used by Alembic.
revision: str = "66642bc11750"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Step 1: Create tables without foreign keys
    op.create_table(
        "role",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column(
            "permissions",
            postgresql.JSON(astext_type=sa.Text()),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "user",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("first_name", sa.String(), nullable=False),
        sa.Column("last_name", sa.String(), nullable=False),
        sa.Column("role_id", sa.Integer(), nullable=False),
        sa.Column("email", sa.String(), nullable=False),
        sa.Column("is_email_confirmed", sa.Boolean(), nullable=False),
        sa.Column(
            "email_confirmation_token", sa.String(length=50), nullable=True
        ),
        sa.Column(
            "registered_at",
            sa.DateTime(),
            server_default=sa.text("TIMEZONE('utc', now())"),
            nullable=True,
        ),
        sa.Column("hashed_password", postgresql.BYTEA(), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("is_verified", sa.Boolean(), nullable=False),
        sa.Column("tg_id", sa.String(length=20), nullable=True),
        sa.Column(
            "tg_settings",
            postgresql.JSON(astext_type=sa.Text()),
            nullable=True,
        ),
        sa.Column("organization_id", sa.Integer(), nullable=True),
        sa.Column("pathfile", sa.String(), nullable=True),
        sa.Column("github_name", sa.String(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("tg_id"),
    )

    op.create_table(
        "organization",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("description", sa.String(), nullable=False),
        sa.Column("owner_id", sa.Uuid(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "group",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("user_id", sa.Uuid(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "project",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("description", sa.String(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(),
            server_default=sa.text("TIMEZONE('utc', now())"),
            nullable=True,
        ),
        sa.Column("organization_id", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "task",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("description", sa.String(), nullable=False),
        sa.Column("is_done", sa.Boolean(), nullable=False),
        sa.Column(
            "added_at",
            sa.DateTime(),
            server_default=sa.text("TIMEZONE('utc', now())"),
            nullable=True,
        ),
        sa.Column("end_date", sa.DateTime(), nullable=True),
        sa.Column("done_at", sa.DateTime(), nullable=True),
        sa.Column("assigner_id", sa.Uuid(), nullable=True),
        sa.Column("duration", sa.Interval(), nullable=True),
        sa.Column("color", sa.String(), nullable=False),
        sa.Column(
            "difficulty",
            sa.Enum(
                "easy", "medium", "hard", "challenging", name="difficulty"
            ),
            nullable=True,
        ),
        sa.Column("project_id", sa.Integer(), nullable=True),
        sa.Column("group_id", sa.Integer(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "user_task",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column(
            "github_data",
            postgresql.JSON(astext_type=sa.Text()),
            nullable=True,
        ),
        sa.Column("task_id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Uuid(), nullable=False),
        sa.Column("is_employee", sa.Boolean(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )

    # Step 2: Add foreign keys
    op.create_foreign_key(
        None, "user", "organization", ["organization_id"], ["id"]
    )
    op.create_foreign_key(None, "user", "role", ["role_id"], ["id"])
    op.create_foreign_key(
        None, "organization", "user", ["owner_id"], ["id"], ondelete="CASCADE"
    )
    op.create_foreign_key(None, "group", "user", ["user_id"], ["id"])
    op.create_foreign_key(
        None,
        "project",
        "organization",
        ["organization_id"],
        ["id"],
        ondelete="CASCADE",
    )
    op.create_foreign_key(
        None, "task", "user", ["assigner_id"], ["id"], ondelete="CASCADE"
    )
    op.create_foreign_key(None, "task", "group", ["group_id"], ["id"])
    op.create_foreign_key(
        None, "task", "project", ["project_id"], ["id"], ondelete="CASCADE"
    )
    op.create_foreign_key(None, "user_task", "task", ["task_id"], ["id"])
    op.create_foreign_key(None, "user_task", "user", ["user_id"], ["id"])

    # Insert roles
    roles = [
        {
            "name": "unauthorized",
            "permissions": {
                "user": {
                    "create": True,
                    "read": False,
                    "update": False,
                    "delete": False,
                },
                "task": {
                    "create": False,
                    "read": False,
                    "update": False,
                    "delete": False,
                },
                "group": {
                    "create": False,
                    "read": False,
                    "update": False,
                    "delete": False,
                },
                "project": {
                    "create": False,
                    "read": False,
                    "update": False,
                    "delete": False,
                },
                "organization": {
                    "create": False,
                    "read": False,
                    "update": False,
                    "delete": False,
                },
                "role": {
                    "create": False,
                    "read": False,
                    "update": False,
                    "delete": False,
                },
            },
        },
        {
            "name": "user",
            "permissions": {
                "user": {
                    "create": True,
                    "read": True,
                    "update": True,
                    "delete": True,
                },
                "task": {
                    "create": True,
                    "read": True,
                    "update": True,
                    "delete": True,
                },
                "group": {
                    "create": True,
                    "read": True,
                    "update": True,
                    "delete": True,
                },
                "project": {
                    "create": True,
                    "read": True,
                    "update": True,
                    "delete": True,
                },
                "organization": {
                    "create": False,
                    "read": False,
                    "update": False,
                    "delete": False,
                },
                "role": {
                    "create": False,
                    "read": False,
                    "update": False,
                    "delete": False,
                },
            },
        },
        {
            "name": "enterprise",
            "permissions": {
                "user": {
                    "create": True,
                    "read": True,
                    "update": True,
                    "delete": True,
                },
                "task": {
                    "create": True,
                    "read": True,
                    "update": True,
                    "delete": True,
                },
                "group": {
                    "create": True,
                    "read": True,
                    "update": True,
                    "delete": True,
                },
                "project": {
                    "create": True,
                    "read": True,
                    "update": True,
                    "delete": True,
                },
                "organization": {
                    "create": True,
                    "read": True,
                    "update": True,
                    "delete": True,
                },
                "role": {
                    "create": False,
                    "read": False,
                    "update": False,
                    "delete": False,
                },
            },
        },
        {
            "name": "admin",
            "permissions": {
                "user": {
                    "create": True,
                    "read": True,
                    "update": True,
                    "delete": True,
                },
                "task": {
                    "create": True,
                    "read": True,
                    "update": True,
                    "delete": True,
                },
                "group": {
                    "create": True,
                    "read": True,
                    "update": True,
                    "delete": True,
                },
                "project": {
                    "create": True,
                    "read": True,
                    "update": True,
                    "delete": True,
                },
                "organization": {
                    "create": True,
                    "read": True,
                    "update": True,
                    "delete": True,
                },
                "role": {
                    "create": True,
                    "read": True,
                    "update": True,
                    "delete": True,
                },
            },
        },
    ]

    op.bulk_insert(
        sa.table(
            "role",
            sa.Column("name", sa.String),
            sa.Column("permissions", JSON),
        ),
        roles,
    )

    # Insert admin user
    admin_user = {
        "id": uuid4(),
        "first_name": "admin",
        "last_name": "admin",
        "role_id": 4,
        "email": "admin@admin.com",
        "is_email_confirmed": True,
        "registered_at": datetime.utcnow(),
        "hashed_password": hash_password(API_ADMIN_PWD),
        "is_active": True,
        "is_verified": True,
        "tg_id": None,
        "tg_settings": None,
        "organization_id": None,
        "pathfile": None,
        "github_name": None,
    }

    op.bulk_insert(
        sa.table(
            "user",
            sa.Column("id", UUID(as_uuid=True)),
            sa.Column("first_name", sa.String),
            sa.Column("last_name", sa.String),
            sa.Column("role_id", sa.Integer),
            sa.Column("email", sa.String),
            sa.Column("is_email_confirmed", sa.Boolean),
            sa.Column("registered_at", sa.DateTime),
            sa.Column("hashed_password", BYTEA),
            sa.Column("is_active", sa.Boolean),
            sa.Column("is_verified", sa.Boolean),
            sa.Column("tg_id", sa.String),
            sa.Column("tg_settings", JSON),
            sa.Column("organization_id", sa.Integer),
            sa.Column("pathfile", sa.String),
            sa.Column("github_name", sa.String),
        ),
        [admin_user],
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("user_task")
    op.drop_table("task")
    op.drop_table("project")
    op.drop_table("group")
    op.drop_table("organization")
    op.drop_table("user")
    op.drop_table("role")
    # ### end Alembic commands ###
