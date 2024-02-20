"""Initial migration

Revision ID: 26eb64b3fb7c
Revises: 
Create Date: 2024-02-19 13:12:05.970625

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '26eb64b3fb7c'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('tracks',
                    sa.Column('id', sa.UUID(), nullable=False),
                    sa.Column('name', sa.String(), nullable=False),
                    sa.Column('author', sa.String(), nullable=False),
                    sa.Column('genre', sa.String(), nullable=False),
                    sa.Column('description', sa.String(), nullable=False),
                    sa.PrimaryKeyConstraint('id')
                    )


def downgrade() -> None:
    op.drop_table('tracks')
