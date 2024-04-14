"""add last few columns to posts table

Revision ID: 6674ba5e5925
Revises: f8c951d4768c
Create Date: 2024-01-02 19:25:36.721801

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "6674ba5e5925"
down_revision: Union[str, None] = "f8c951d4768c"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column(
        "posts",
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),)
    op.add_column("posts",sa.Column(
            "published", sa.Boolean(), nullable=False, server_default="True"
        )
    )


def downgrade():
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')
