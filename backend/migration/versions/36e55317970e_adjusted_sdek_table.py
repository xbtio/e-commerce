"""adjusted sdek table

Revision ID: 36e55317970e
Revises: cc45b32e7d76
Create Date: 2023-11-15 05:54:52.032310

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '36e55317970e'
down_revision: Union[str, None] = 'cc45b32e7d76'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('order_requests', sa.Column('order_status', sa.String(length=150), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('order_requests', 'order_status')
    # ### end Alembic commands ###
