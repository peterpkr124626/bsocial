"""add content column to posts table.

Revision ID: ae30cad45fc8
Revises: fd8961b13160
Create Date: 2022-07-15 11:00:31.649848

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ae30cad45fc8'
down_revision = 'fd8961b13160'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("content", sa.String, nullable=False))


def downgrade() -> None:
    op.drop_column("posts", "content")
