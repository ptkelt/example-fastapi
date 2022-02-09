"""add foreign-key to posts table

Revision ID: a5821715f60d
Revises: e13d5eb500b6
Create Date: 2022-02-09 12:13:24.970506

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a5821715f60d'
down_revision = 'e13d5eb500b6'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('post_users_fk', source_table="posts", referent_table="users",
        local_cols=['owner_id'], remote_cols=['id'], ondelete="CASCADE")
    pass


def downgrade():
    op.drop_constraint('post_users_fk', 'posts')
    op.drop_column('posts', 'owner_id')
    pass
