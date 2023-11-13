"""added new constraint

Revision ID: 030efc1fe7d1
Revises: 1cea6d78be53
Create Date: 2023-11-11 21:44:49.029313

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '030efc1fe7d1'
down_revision: Union[str, None] = '1cea6d78be53'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('shopping_cart_item_product_id_fkey', 'shopping_cart_item', type_='foreignkey')
    op.create_foreign_key(None, 'shopping_cart_item', 'product', ['product_id'], ['id'], ondelete='cascade')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'shopping_cart_item', type_='foreignkey')
    op.create_foreign_key('shopping_cart_item_product_id_fkey', 'shopping_cart_item', 'product', ['product_id'], ['id'])
    # ### end Alembic commands ###