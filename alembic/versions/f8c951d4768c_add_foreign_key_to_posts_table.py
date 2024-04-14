"""add foreign key to posts table

Revision ID: f8c951d4768c
Revises: 02a5f7354b66
Create Date: 2024-01-02 19:14:26.838903

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f8c951d4768c'
down_revision: Union[str, None] = '02a5f7354b66'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column('posts', sa.Column('owner_id',sa.Integer(), nullable=False))
    op.create_foreign_key('posts_users_fk', source_table = 'posts', referent_table = 'users', local_cols = ['owner_id'], remote_cols = ['id'], ondelete ="CASCADE")

    pass


def downgrade():
    op.drop_constraint('posts_users_fk', table_name = 'posts')
    op.drop_column('posts', 'owner_id')
    pass
