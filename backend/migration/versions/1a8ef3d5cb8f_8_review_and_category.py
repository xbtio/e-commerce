"""8 review and category

Revision ID: 1a8ef3d5cb8f
Revises: 2b6f022c84a8
Create Date: 2023-10-21 01:38:06.389272

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1a8ef3d5cb8f'
down_revision: Union[str, None] = '2b6f022c84a8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('category',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=150), nullable=False),
    sa.Column('description', sa.String(length=350), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column('product', sa.Column('category_id', sa.Integer(), nullable=False))
    op.add_column('product', sa.Column('rating', sa.Float(), nullable=False, server_default='0.0'))
    op.add_column('product', sa.Column('number_of_ratings', sa.Integer(), nullable=False, server_default='0'))
    op.create_foreign_key(None, 'product', 'category', ['category_id'], ['id'])
    op.add_column('user', sa.Column('name', sa.String(length=150), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'name')
    op.drop_constraint(None, 'product', type_='foreignkey')
    op.drop_column('product', 'number_of_ratings')
    op.drop_column('product', 'rating')
    op.drop_column('product', 'category_id')
    op.drop_table('category')
    # ### end Alembic commands ###
