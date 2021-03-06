"""empty message

Revision ID: a3294373334d
Revises: 
Create Date: 2018-03-07 15:22:07.997671

"""
from alembic import op
import sqlalchemy as sa
import uuid


# revision identifiers, used by Alembic.
revision = 'a3294373334d'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    role_table = op.create_table('roles',
    sa.Column('id', sa.String(length=36), nullable=False),
    sa.Column('name', sa.String(length=32), nullable=True),
    sa.Column('description', sa.String(length=128), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('schools',
    sa.Column('id', sa.String(length=36), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('describe', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users',
    sa.Column('id', sa.String(length=36), nullable=False),
    sa.Column('username', sa.String(length=36), nullable=False),
    sa.Column('password', sa.String(length=128), nullable=False),
    sa.Column('firstname', sa.String(length=36), nullable=True),
    sa.Column('lastname', sa.String(length=36), nullable=True),
    sa.Column('email', sa.String(length=128), nullable=True),
    sa.Column('phone', sa.String(length=64), nullable=True),
    sa.Column('enabled', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('courses',
    sa.Column('id', sa.String(length=36), nullable=False),
    sa.Column('name', sa.String(length=128), nullable=True),
    sa.Column('description', sa.String(length=256), nullable=True),
    sa.Column('fee', sa.Float(), nullable=True),
    sa.Column('school_id', sa.String(length=36), nullable=True),
    sa.ForeignKeyConstraint(['school_id'], ['schools.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user_roles',
    sa.Column('id', sa.String(length=36), nullable=False),
    sa.Column('user_id', sa.String(length=36), nullable=True),
    sa.Column('role_id', sa.String(length=36), nullable=True),
    sa.Column('school_id', sa.String(length=36), nullable=True),
    sa.ForeignKeyConstraint(['role_id'], ['roles.id'], ),
    sa.ForeignKeyConstraint(['school_id'], ['schools.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('course_users',
    sa.Column('id', sa.String(length=36), nullable=False),
    sa.Column('user_id', sa.String(length=36), nullable=True),
    sa.Column('course_id', sa.String(length=36), nullable=True),
    sa.ForeignKeyConstraint(['course_id'], ['courses.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('payments',
    sa.Column('id', sa.String(length=36), nullable=False),
    sa.Column('user_id', sa.String(length=36), nullable=True),
    sa.Column('course_id', sa.String(length=36), nullable=True),
    sa.Column('payment', sa.Float(), nullable=True),
    sa.Column('created_on', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated_on', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.ForeignKeyConstraint(['course_id'], ['courses.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )

    id1 = uuid.uuid4()
    id2 = uuid.uuid4()
    id3 = uuid.uuid4()
    op.bulk_insert(role_table,
       [
           {'id': id1, 'name': 'admin', 'description': 'admin'},
           {'id': id2, 'name': 'staff', 'description': 'staff'},
           {'id': id3, 'name': 'student', 'description': 'student'},
       ]
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('payments')
    op.drop_table('course_users')
    op.drop_table('user_roles')
    op.drop_table('courses')
    op.drop_table('users')
    op.drop_table('schools')
    op.drop_table('roles')
    # ### end Alembic commands ###
