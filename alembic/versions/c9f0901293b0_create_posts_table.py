"""create posts table

Revision ID: c9f0901293b0
Revises: 
Create Date: 2022-02-09 11:53:51.933393

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c9f0901293b0'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('posts', 
        sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
        sa.Column('title', sa.String(), nullable=False)
    )   
    pass


def downgrade():
    op.drop_table('posts')
    pass
