"""create users table.

Revision ID: f7e10cc66aee
Revises: ae30cad45fc8
Create Date: 2022-07-15 11:08:44.562650

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
from sqlalchemy import text

revision = 'f7e10cc66aee'
down_revision = 'ae30cad45fc8'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table("users", sa.Column("id", sa.Integer(), nullable=False),
                    sa.Column("email", sa.String, nullable=False), sa.Column("password", sa.String, nullable=False),
                    sa.Column("created_at", sa.TIMESTAMP(timezone=True), server_default=text("NOW()"), nullable=False),
                    sa.PrimaryKeyConstraint("id"), sa.UniqueConstraint("email"))


def downgrade() -> None:
    op.drop_table("users")
