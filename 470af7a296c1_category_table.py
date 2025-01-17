"""category table

Revision ID: 470af7a296c1
Revises: 
Create Date: 2025-01-15 16:56:04.190530

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import INTEGER, VARCHAR, NVARCHAR, Column, TIMESTAMP, func

# revision identifiers, used by Alembic.
revision: str = '470af7a296c1'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
    "category",
    Column("id", INTEGER, primary_key=True),
    Column("name", VARCHAR(30), nullable=False),
    Column("description", VARCHAR(255)),
    Column("timestamp", TIMESTAMP, server_default=func.now()),
)


def downgrade() -> None:
    op.drop_table('account')
