"""empty message

Revision ID: dc3f7a6e512b
Revises: 928117998999
Create Date: 2024-02-01 00:24:25.475139

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'dc3f7a6e512b'
down_revision: Union[str, None] = '928117998999'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('t_users', sa.Column('user_id', sa.TEXT(), nullable=False))
    op.drop_constraint('t_users_username_key', 't_users', type_='unique')
    op.create_unique_constraint(None, 't_users', ['user_id'])
    op.drop_constraint('t_users_prefecture_id_fkey', 't_users', type_='foreignkey')
    op.drop_column('t_users', 'username')
    op.drop_column('t_users', 'password')
    op.drop_column('t_users', 'tel')
    op.drop_column('t_users', 'postal_code')
    op.drop_column('t_users', 'point_possessed')
    op.drop_column('t_users', 'prefecture_id')
    op.drop_column('t_users', 'last_name')
    op.drop_column('t_users', 'email')
    op.drop_column('t_users', 'first_name')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('t_users', sa.Column('first_name', sa.VARCHAR(length=100), autoincrement=False, nullable=False))
    op.add_column('t_users', sa.Column('email', sa.VARCHAR(length=100), autoincrement=False, nullable=False))
    op.add_column('t_users', sa.Column('last_name', sa.VARCHAR(length=100), autoincrement=False, nullable=False))
    op.add_column('t_users', sa.Column('prefecture_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.add_column('t_users', sa.Column('point_possessed', sa.INTEGER(), autoincrement=False, nullable=False))
    op.add_column('t_users', sa.Column('postal_code', sa.VARCHAR(length=8), autoincrement=False, nullable=True))
    op.add_column('t_users', sa.Column('tel', sa.VARCHAR(length=100), autoincrement=False, nullable=True))
    op.add_column('t_users', sa.Column('password', sa.VARCHAR(length=128), autoincrement=False, nullable=False))
    op.add_column('t_users', sa.Column('username', sa.TEXT(), autoincrement=False, nullable=False))
    op.create_foreign_key('t_users_prefecture_id_fkey', 't_users', 'm_prefectures', ['prefecture_id'], ['prefecture_id'])
    op.drop_constraint(None, 't_users', type_='unique')
    op.create_unique_constraint('t_users_username_key', 't_users', ['username'])
    op.drop_column('t_users', 'user_id')
    # ### end Alembic commands ###