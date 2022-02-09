"""add content column

Revision ID: 1384288613ce
Revises: c9f0901293b0
Create Date: 2022-02-09 12:03:29.706804

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1384288613ce'
down_revision = 'c9f0901293b0'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column('posts', 'content')
    pass
