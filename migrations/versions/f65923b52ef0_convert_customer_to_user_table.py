"""convert customer to user table

Revision ID: f65923b52ef0
Revises: 5b4437529e47
Create Date: 2023-05-28 08:35:33.300739

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision = 'f65923b52ef0'
down_revision = '5b4437529e47'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.rename_table("customer", "users")
    user_type_enum = postgresql.ENUM("customer", "admin", "super_admin", name="user_type")
    user_type_enum.create(op.get_bind(), checkfirst=True)
    op.add_column("users", sa.Column("user_type", user_type_enum, server_default="customer"))


def downgrade() -> None:
    op.drop_column("users", "user_type")
    op.rename_table("users", "customer")
    user_type_enum = postgresql.ENUM("customer", "admin", "super_admin", name="user_type")
    user_type_enum.drop(op.get_bind())

