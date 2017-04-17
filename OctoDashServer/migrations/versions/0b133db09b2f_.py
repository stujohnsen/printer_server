"""empty message

Revision ID: 0b133db09b2f
Revises: 
Create Date: 2017-04-14 18:01:11.911545

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '0b133db09b2f'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('roles',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=60), nullable=True),
    sa.Column('description', sa.String(length=200), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=60), nullable=True),
    sa.Column('username', sa.String(length=60), nullable=True),
    sa.Column('first_name', sa.String(length=60), nullable=True),
    sa.Column('last_name', sa.String(length=60), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.Column('role_id', sa.Integer(), nullable=True),
    sa.Column('is_admin', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['role_id'], ['roles.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_index(op.f('ix_users_first_name'), 'users', ['first_name'], unique=False)
    op.create_index(op.f('ix_users_last_name'), 'users', ['last_name'], unique=False)
    op.create_index(op.f('ix_users_username'), 'users', ['username'], unique=True)
    op.drop_table('printers')
    op.drop_table('info')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('info',
    sa.Column('printer_id', mysql.INTEGER(display_width=11), nullable=False),
    sa.Column('x_api_key', mysql.VARCHAR(length=128), nullable=True),
    sa.Column('ip_address', mysql.VARCHAR(length=64), nullable=True),
    sa.Column('camera_rotation', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('printer_id'),
    mysql_default_charset=u'latin1',
    mysql_engine=u'InnoDB'
    )
    op.create_table('printers',
    sa.Column('printer_id', mysql.INTEGER(display_width=11), nullable=False),
    sa.Column('url', mysql.VARCHAR(length=1024), nullable=True),
    sa.Column('x_api_key', mysql.VARCHAR(length=1024), nullable=True),
    sa.Column('camera_rotation', mysql.SMALLINT(display_width=6), autoincrement=False, nullable=True),
    sa.Column('printer_name', mysql.VARCHAR(length=1024), nullable=True),
    sa.Column('printer_type', mysql.VARCHAR(length=1024), nullable=True),
    sa.PrimaryKeyConstraint('printer_id'),
    mysql_default_charset=u'latin1',
    mysql_engine=u'InnoDB'
    )
    op.drop_index(op.f('ix_users_username'), table_name='users')
    op.drop_index(op.f('ix_users_last_name'), table_name='users')
    op.drop_index(op.f('ix_users_first_name'), table_name='users')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users')
    op.drop_table('roles')
    # ### end Alembic commands ###