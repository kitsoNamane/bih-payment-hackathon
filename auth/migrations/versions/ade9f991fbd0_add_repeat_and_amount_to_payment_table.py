"""add repeat and amount to payment table

Revision ID: ade9f991fbd0
Revises: 65550a43b21a
Create Date: 2023-05-29 21:53:41.009863

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision = 'ade9f991fbd0'
down_revision = '65550a43b21a'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("payments", sa.Column("amount", postgresql.MONEY()))
    op.add_column("payments", sa.Column("repeat", sa.String))
    op.add_column("payments", sa.Column("payment_type", sa.String))

def downgrade() -> None:
    op.drop_column("payments", "amount")
    op.drop_column("payments", "repeat")
    op.drop_column("payments", "payment_type")
