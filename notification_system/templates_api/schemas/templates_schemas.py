from datetime import datetime
from enum import Enum
from typing import Self
from uuid import UUID

from pydantic import BaseModel, model_validator

from notification_system.common_utils.types.jinja2_pydantic_schema import (
    Jinja2Template
)


class Channel(str, Enum):
    SMS = 'SMS'
    EMAIL = 'EMAIL'
    MOBILE_PUSH = 'MOBILE_PUSH'
    WEB_PUSH = 'WEB_PUSH'
    WEB_SOCKET = 'WEB_SOCKET'


class EmailTemplate(BaseModel):
    content: Jinja2Template
    subject: Jinja2Template
    version: str


class SMSTemplate(BaseModel):
    content: Jinja2Template
    version: str


class GenericTemplate(BaseModel):
    title: Jinja2Template | None = None
    content: Jinja2Template
    version: str


TemplateType = EmailTemplate | SMSTemplate | GenericTemplate


class RegisterTemplate(BaseModel):
    id: UUID
    template_name: str
    channel_type: Channel
    template: TemplateType
    tenant_id: UUID
    version: str

    @model_validator(mode='after')
    def check_channel_and_template_model(self) -> Self:
        if self.channel_type == Channel.EMAIL and isinstance(
            self.template, EmailTemplate
        ):
            return self
        if self.channel_type == Channel.SMS and isinstance(
            self.template, SMSTemplate
        ):
            return self
        raise ValueError('Channel and TemplateType must be compatible')


class Template(RegisterTemplate):
    context_keys_content: list[str] | None
    context_keys_subject: list[str] | None
    create_at: datetime
    updated_at: datetime | None = None


class TemplateSumary(BaseModel):
    id: UUID
    template_name: str
    channel: Channel


class TemplateSumaryList(BaseModel):
    templates: list[TemplateSumary]
