"""add user table

Revision ID: e13d5eb500b6
Revises: 1384288613ce
Create Date: 2022-02-09 12:07:05.326120

"""
from http import server
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e13d5eb500b6'
down_revision = '1384288613ce'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('password', sa.String(), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True),
            server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email')
    )
    pass


def downgrade():
    op.drop_table('users')
    pass
