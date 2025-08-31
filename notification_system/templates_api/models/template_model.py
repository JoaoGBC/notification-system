from datetime import datetime
from enum import Enum
from uuid import UUID
from sqlalchemy import JSON, TEXT, func, text
from sqlalchemy.orm import Mapped, mapped_column

from ..db_registry import table_registry


class Channel(str, Enum):
    SMS = 'SMS'
    EMAIL = 'EMAIL'
    MOBILE_PUSH = 'MOBILE_PUSH'
    WEB_PUSH = 'WEB_PUSH'
    WEB_SOCKET = 'WEB_SOCKET'


@table_registry.mapped_as_dataclass
class TemplateDb:
    __tablename__ = 'templates'
    id: Mapped[UUID] = mapped_column(
        init=False,
        primary_key=True,
        index=True,
        server_default=text("uuid_generate_v4()")
    )
    template_name: Mapped[str]
    channel: Mapped[Channel] = mapped_column(index=True)
    
    
    version: Mapped[str]
    tenant_id: Mapped[UUID] = mapped_column(nullable=False, unique=False)
    created_at: Mapped[datetime] = mapped_column(
        init=False,
        server_default=func.now()
    )
    updated_at: Mapped[datetime | None] = mapped_column(
        init=False,
        nullable=True,
        server_onupdate=func.now()
    )

    html_content: Mapped[str | None] = mapped_column(TEXT, nullable=True, default=None)
    subject: Mapped[str | None] = mapped_column(nullable=True, default=None)
    sms_content: Mapped[str | None] = mapped_column(nullable=True, default=None)
    generic_title_content: Mapped[str | None] = mapped_column(nullable=True, default=None)
    generic_content: Mapped[str | None] = mapped_column(nullable=True, default=None)
    context_keys_content: Mapped[list[str]] = mapped_column(JSON, nullable=True, default=None)
    context_keys_subject: Mapped[list[str]] = mapped_column(JSON, nullable=True, default=None)