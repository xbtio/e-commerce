"""adjusted sdek table

Revision ID: cc45b32e7d76
Revises: ed2f5c5965cb
Create Date: 2023-11-15 04:57:18.480156

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'cc45b32e7d76'
down_revision: Union[str, None] = 'ed2f5c5965cb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('order_requests', sa.Column('user_email', sa.String(length=250), nullable=False))
    op.drop_constraint('order_requests_user_id_fkey', 'order_requests', type_='foreignkey')
    op.drop_column('order_requests', 'user_id')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('order_requests', sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=False))
    op.create_foreign_key('order_requests_user_id_fkey', 'order_requests', 'user', ['user_id'], ['id'])
    op.drop_column('order_requests', 'user_email')
    # ### end Alembic commands ###
