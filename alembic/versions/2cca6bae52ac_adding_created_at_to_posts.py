"""adding created at to posts

Revision ID: 2cca6bae52ac
Revises: a5821715f60d
Create Date: 2022-02-09 12:19:23.469060

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2cca6bae52ac'
down_revision = 'a5821715f60d'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('NOW()')))
    pass


def downgrade():
    op.drop_column('posts', 'created_at')
    pass
