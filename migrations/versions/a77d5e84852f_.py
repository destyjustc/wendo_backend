"""empty message

Revision ID: a77d5e84852f
Revises: abc92150a3aa
Create Date: 2018-03-28 14:39:43.947002

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a77d5e84852f'
down_revision = 'abc92150a3aa'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('clue_groups',
    sa.Column('id', sa.String(length=36), nullable=False),
    sa.Column('created_on', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated_on', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.Column('created_by', sa.String(length=36), nullable=True),
    sa.Column('assigned_to', sa.String(length=36), nullable=True),
    sa.ForeignKeyConstraint(['assigned_to'], ['users.id'], ),
    sa.ForeignKeyConstraint(['created_by'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('clue_groups')
    # ### end Alembic commands ###
