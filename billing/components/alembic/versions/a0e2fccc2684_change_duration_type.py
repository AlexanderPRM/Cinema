"""Change duration TYPE

Revision ID: a0e2fccc2684
Revises: bb42c3e7e8e4
Create Date: 2023-07-16 20:06:50.108510

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "a0e2fccc2684"
down_revision = "bb42c3e7e8e4"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("subscriptions_tiers", sa.Column("duration", sa.Integer(), nullable=False))
    op.drop_column("subscriptions_tiers", "duratation")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "subscriptions_tiers",
        sa.Column("duratation", postgresql.TIMESTAMP(), autoincrement=False, nullable=False),
    )
    op.drop_column("subscriptions_tiers", "duration")
    # ### end Alembic commands ###