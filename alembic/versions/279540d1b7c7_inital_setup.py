"""inital setup

Revision ID: 279540d1b7c7
Revises: 
Create Date: 2024-09-29 09:18:27.028966

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '279540d1b7c7'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('executions',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('timestamp', sa.DateTime(), nullable=False),
    sa.Column('commands', sa.Integer(), nullable=False),
    sa.Column('result', sa.Integer(), nullable=False),
    sa.Column('duration', sa.Float(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_executions_id'), 'executions', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_executions_id'), table_name='executions')
    op.drop_table('executions')
    # ### end Alembic commands ###
