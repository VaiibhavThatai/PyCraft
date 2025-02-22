"""create posts table

Revision ID: 2bafa350baa3
Revises: 
Create Date: 2024-01-02 18:14:51.354158

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2bafa350baa3'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade():
    op.create_table('posts', sa.Column('id', sa.Integer, nullable=False, primary_key=True), sa.Column('title', sa.String, nullable=False))


def downgrade():
    op.drop_table('posts')
