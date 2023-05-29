"""add payments

Revision ID: 65550a43b21a
Revises: 6b6a8b7af331
Create Date: 2023-05-28 14:37:44.885553

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '65550a43b21a'
down_revision = '6b6a8b7af331'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "payments",
        sa.Column("id", sa.Integer, primary_key=True, index=True, autoincrement=True),
        sa.Column("service", sa.String, index=True),
        sa.Column("reference", sa.String, primary_key=True, index=True),
        sa.column("due_date", sa.DateTime),
        sa.Column("paid_status", sa.Boolean, index=True, default=False),
        sa.Column("payer_id", sa.Integer, index=True, unique=True),
        sa.Column("created_at", sa.DateTime),
        )

def downgrade() -> None:
    op.drop_table("payments")



