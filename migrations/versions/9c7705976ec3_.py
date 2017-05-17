"""empty message

Revision ID: 9c7705976ec3
Revises: 7edffa04a6ea
Create Date: 2017-05-17 10:12:40.011329

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9c7705976ec3'
down_revision = '7edffa04a6ea'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('blacklist_tokens',
    sa.Column('token_id', sa.Integer(), nullable=False),
    sa.Column('token', sa.String(length=500), nullable=False),
    sa.Column('blacklisted_on', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('token_id'),
    sa.UniqueConstraint('token')
    )
    op.add_column('users', sa.Column('first_name', sa.String(length=50), nullable=False))
    op.add_column('users', sa.Column('last_name', sa.String(length=50), nullable=False))
    op.add_column('users', sa.Column('password', sa.String(length=50), nullable=False))
    op.drop_column('users', 'password_hash')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('password_hash', sa.VARCHAR(length=50), autoincrement=False, nullable=False))
    op.drop_column('users', 'password')
    op.drop_column('users', 'last_name')
    op.drop_column('users', 'first_name')
    op.drop_table('blacklist_tokens')
    # ### end Alembic commands ###
