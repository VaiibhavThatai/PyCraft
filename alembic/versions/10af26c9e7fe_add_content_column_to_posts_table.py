"""add content column to posts table

Revision ID: 10af26c9e7fe
Revises: 2bafa350baa3
Create Date: 2024-01-02 18:16:41.979451

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '10af26c9e7fe'
down_revision: Union[str, None] = '2bafa350baa3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))


def downgrade():
    op.drop_column('posts', 'content')