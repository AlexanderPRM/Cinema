"""Initial

Revision ID: d7d22ea7a8cd
Revises:
Create Date: 2023-07-09 19:30:11.953349

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "d7d22ea7a8cd"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "transactions",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("user_id", sa.UUID(), nullable=False),
        sa.Column("value", sa.Integer(), nullable=False),
        sa.Column("ttl", sa.DateTime(), nullable=False),
        sa.Column("provider", sa.String(), nullable=False),
        sa.Column("idempotency_key", sa.UUID(), nullable=False),
        sa.Column(
            "operate_status",
            sa.Enum("waiting", "success", "error", "canceled", name="operatestatus"),
            nullable=False,
        ),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("transactions")
    # ### end Alembic commands ###