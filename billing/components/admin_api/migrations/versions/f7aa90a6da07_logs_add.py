"""logs_add

Revision ID: f7aa90a6da07
Revises: 67118f800b6e
Create Date: 2023-07-13 10:05:17.696433

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'f7aa90a6da07'
down_revision = '67118f800b6e'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('transactions_log',
    sa.Column('user_id', sa.UUID(), nullable=False),
    sa.Column('transaction_id', sa.UUID(), nullable=False),
    sa.Column('value', sa.Integer(), nullable=False),
    sa.Column('provider', sa.String(), nullable=False),
    sa.Column('idempotency_key_ttl', sa.DateTime(), nullable=False),
    sa.Column('idempotency_key', sa.UUID(), nullable=False),
    sa.Column('operate_status', postgresql.ENUM('SUCCESS', 'ERROR', 'WAITING', name='status_enum'), nullable=True),
    sa.Column('payment_details', sa.String(), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
    sa.PrimaryKeyConstraint('user_id', 'transaction_id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('transactions_log')
    # ### end Alembic commands ###