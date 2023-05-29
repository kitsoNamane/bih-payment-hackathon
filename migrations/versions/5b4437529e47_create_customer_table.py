"""create customer table
Revision ID: 5b4437529e47
Revises: 
Create Date: 2023-05-27 13:58:35.265866

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5b4437529e47'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
    "customer",
    sa.Column("id", sa.UUID, primary_key=True, index=True),
    sa.Column("phone_number", sa.Integer, unique=True, index=True),
    sa.Column("national_id", sa.Integer, unique=True, index=True),
    sa.Column("password", sa.String, nullable=False),
    )


def downgrade() -> None:
    op.drop_table("customer")
