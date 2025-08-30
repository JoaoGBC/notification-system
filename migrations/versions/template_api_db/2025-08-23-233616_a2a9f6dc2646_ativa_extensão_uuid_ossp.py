"""ativa extensão uuid-ossp

Revision ID: a2a9f6dc2646
Revises: 
Create Date: 2025-08-23 23:36:16.818306

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a2a9f6dc2646'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


transactional = False

def upgrade() -> None:
    op.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp";')
    op.execute('CREATE SCHEMA IF NOT EXISTS "templates_api_schema";')

def downgrade() -> None:
    op.execute('DROP EXTENSION IF EXISTS "uuid-ossp";')
