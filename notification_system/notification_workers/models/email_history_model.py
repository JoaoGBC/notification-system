from datetime import datetime
from uuid import UUID

from sqlalchemy import TEXT, func, text
from sqlalchemy.orm import Mapped, mapped_column

from ..db_registry import table_registry


@table_registry.mapped_as_dataclass
class EmailHistory:
    __tablename__ = 'email_history'
    id: Mapped[UUID] = mapped_column(
        init=False,
        primary_key=True,
        index=True,
        server_default=text('uuid_generate_v4()'),
    )
    sent_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now(), primary_key=True
    )

    template_id: Mapped[UUID]
    recipient: Mapped[str]

    html_content: Mapped[str | None] = mapped_column(
        TEXT, nullable=True, default=None
    )
    subject: Mapped[str | None] = mapped_column(nullable=True, default=None)
