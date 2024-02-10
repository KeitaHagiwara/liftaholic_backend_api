"""empty message

Revision ID: 39349986d8a5
Revises: a4d75c1ca4b4
Create Date: 2024-02-02 19:19:18.203101

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '39349986d8a5'
down_revision: Union[str, None] = 'a4d75c1ca4b4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('t_user_trainings')
    op.add_column('m_difficulty', sa.Column('id', sa.INTEGER(), nullable=False))
    op.add_column('m_difficulty', sa.Column('difficulty_no', sa.INTEGER(), nullable=False))
    op.create_unique_constraint(None, 'm_difficulty', ['difficulty_no'])
    op.drop_column('m_difficulty', 'difficulty_id')
    op.add_column('m_effectiveness', sa.Column('id', sa.INTEGER(), nullable=False))
    op.add_column('m_effectiveness', sa.Column('effectiveness_no', sa.INTEGER(), nullable=False))
    op.create_unique_constraint(None, 'm_effectiveness', ['effectiveness_no'])
    op.drop_column('m_effectiveness', 'effectiveness_id')
    op.add_column('m_event', sa.Column('id', sa.INTEGER(), nullable=False))
    op.add_column('m_event', sa.Column('event_no', sa.INTEGER(), nullable=False))
    op.create_unique_constraint(None, 'm_event', ['event_no'])
    op.drop_column('m_event', 'event_id')
    op.add_column('m_part', sa.Column('id', sa.INTEGER(), nullable=False))
    op.add_column('m_part', sa.Column('part_no', sa.INTEGER(), nullable=False))
    op.create_unique_constraint(None, 'm_part', ['part_no'])
    op.drop_column('m_part', 'part_id')
    op.add_column('m_purpose', sa.Column('id', sa.INTEGER(), nullable=False))
    op.add_column('m_purpose', sa.Column('purpose_no', sa.INTEGER(), nullable=False))
    op.create_unique_constraint(None, 'm_purpose', ['purpose_no'])
    op.drop_column('m_purpose', 'purpose_id')
    op.add_column('m_type', sa.Column('id', sa.INTEGER(), nullable=False))
    op.add_column('m_type', sa.Column('type_no', sa.INTEGER(), nullable=False))
    op.create_unique_constraint(None, 'm_type', ['type_no'])
    op.drop_column('m_type', 'type_id')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('m_type', sa.Column('type_id', sa.INTEGER(), autoincrement=True, nullable=False))
    op.drop_constraint(None, 'm_type', type_='unique')
    op.drop_column('m_type', 'type_no')
    op.drop_column('m_type', 'id')
    op.add_column('m_purpose', sa.Column('purpose_id', sa.INTEGER(), autoincrement=True, nullable=False))
    op.drop_constraint(None, 'm_purpose', type_='unique')
    op.drop_column('m_purpose', 'purpose_no')
    op.drop_column('m_purpose', 'id')
    op.add_column('m_part', sa.Column('part_id', sa.INTEGER(), autoincrement=True, nullable=False))
    op.drop_constraint(None, 'm_part', type_='unique')
    op.drop_column('m_part', 'part_no')
    op.drop_column('m_part', 'id')
    op.add_column('m_event', sa.Column('event_id', sa.INTEGER(), autoincrement=True, nullable=False))
    op.drop_constraint(None, 'm_event', type_='unique')
    op.drop_column('m_event', 'event_no')
    op.drop_column('m_event', 'id')
    op.add_column('m_effectiveness', sa.Column('effectiveness_id', sa.INTEGER(), autoincrement=True, nullable=False))
    op.drop_constraint(None, 'm_effectiveness', type_='unique')
    op.drop_column('m_effectiveness', 'effectiveness_no')
    op.drop_column('m_effectiveness', 'id')
    op.add_column('m_difficulty', sa.Column('difficulty_id', sa.INTEGER(), autoincrement=True, nullable=False))
    op.drop_constraint(None, 'm_difficulty', type_='unique')
    op.drop_column('m_difficulty', 'difficulty_no')
    op.drop_column('m_difficulty', 'id')
    op.create_table('t_user_trainings',
    sa.Column('training_plan_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('training_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('created_at', postgresql.TIMESTAMP(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), autoincrement=False, nullable=False, comment='登録日時'),
    sa.Column('updated_at', postgresql.TIMESTAMP(timezone=True), autoincrement=False, nullable=True, comment='最終更新日時'),
    sa.ForeignKeyConstraint(['training_plan_id'], ['t_training_plans.id'], name='t_user_trainings_training_plan_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='t_user_trainings_pkey')
    )
    # ### end Alembic commands ###