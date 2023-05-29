"""add email column

Revision ID: 6b6a8b7af331
Revises: f65923b52ef0
Create Date: 2023-05-28 10:18:41.701983

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6b6a8b7af331'
down_revision = 'f65923b52ef0'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("users", sa.Column("email", sa.String, unique=True))

def downgrade() -> None:
    op.drop_column("users", "email")
