"""create review table

Revision ID: 2ec9e22cb975
Revises: ab4aa19befb7
Create Date: 2024-11-08 10:41:11.725728

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '2ec9e22cb975'
down_revision: Union[str, None] = 'ab4aa19befb7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Reviews',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('review_text', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('rating', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Uuid(), nullable=True),
    sa.Column('book_id', sa.Uuid(), nullable=True),
    sa.Column('created_at', postgresql.TIMESTAMP(), nullable=True),
    sa.Column('updated_at', postgresql.TIMESTAMP(), nullable=True),
    sa.ForeignKeyConstraint(['book_id'], ['Books.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['Users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('Reviews')
    # ### end Alembic commands ###
