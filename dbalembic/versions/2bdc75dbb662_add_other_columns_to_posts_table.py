"""add other columns to posts table.

Revision ID: 2bdc75dbb662
Revises: be33e98c0f16
Create Date: 2022-07-15 11:22:26.000218

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
from sqlalchemy import text

revision = '2bdc75dbb662'
down_revision = 'be33e98c0f16'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("published", sa.Boolean, nullable=False, server_default=text("TRUE")))
    op.add_column("posts",
                  sa.Column("created_at", sa.TIMESTAMP(timezone=True), nullable=False, server_default=text("NOW()")))


def downgrade() -> None:
    op.drop_column("posts", "published")
    op.drop_column("posts", "created_at")
