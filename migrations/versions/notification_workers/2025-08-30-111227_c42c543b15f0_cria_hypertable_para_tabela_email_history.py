"""cria hypertable para tabela email_history

Revision ID: c42c543b15f0
Revises: 0ad8cd4eac41
Create Date: 2025-08-30 11:12:27.862038

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c42c543b15f0'
down_revision: Union[str, Sequence[str], None] = '0ad8cd4eac41'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(
        """
        SELECT create_hypertable(
            'notification_workers_schema.email_history',
            'sent_at',
            if_not_exists => TRUE
        );
        """
    )
   

def downgrade() -> None:
    op.execute("SELECT 1;")
    print("Downgrade de 'create_hypertable' não reverte a tabela para uma tabela padrão. A migração anterior cuidará do drop da tabela se necessário.")


    
