"""empty message

Revision ID: 5ace30e8e30c
Revises: 9ec877021343
Create Date: 2023-11-29 11:26:36.468958

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5ace30e8e30c'
down_revision = '9ec877021343'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('posts',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=300), nullable=False),
    sa.Column('url', sa.String(length=300), nullable=False),
    sa.Column('publisher', sa.String(length=100), nullable=False),
    sa.Column('publisher_url', sa.String(length=300), nullable=True),
    sa.Column('created_utc', sa.DateTime(), nullable=False),
    sa.Column('category', sa.String(length=100), nullable=False),
    sa.Column('other', sa.String(length=100), nullable=True),
    sa.Column('status', sa.Enum('Unread', 'Filtered', 'Not relevant', 'Relevant'), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('url')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('password', sa.String(), nullable=False),
    sa.Column('created_on', sa.DateTime(), nullable=False),
    sa.Column('is_admin', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users')
    op.drop_table('posts')
    # ### end Alembic commands ###
