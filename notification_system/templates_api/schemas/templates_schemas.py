from datetime import datetime
from enum import Enum
from uuid import UUID

from pydantic import BaseModel


class Channel(str, Enum):
    SMS = 'SMS'
    EMAIL = 'EMAIL'
    MOBILE_PUSH = 'MOBILE_PUSH'
    WEB_PUSH = 'WEB_PUSH'
    WEB_SOCKET = 'WEB_SOCKET'


class EmailTemplate(BaseModel):
    content: str
    subject: str
    version: str


class SMSTemplate(BaseModel):
    content: str
    version: str


class GenericTemplate(BaseModel):
    title: str | None = None
    content: str
    version: str


TemplateType = EmailTemplate | SMSTemplate | GenericTemplate


class RegisterTemplate(BaseModel):
    id: UUID
    template_name: str
    channel_type: Channel
    template: TemplateType
    tenant_id: UUID
    version: str


class Template(RegisterTemplate):
    create_at: datetime
    updated_at: datetime | None = None
