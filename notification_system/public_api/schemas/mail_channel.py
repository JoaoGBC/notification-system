from uuid import UUID
from pydantic import BaseModel, EmailStr, ConfigDict
from enum import Enum

from notification_system.common_utils.types.jinja2_pydantic_schema import (
    Jinja2Template
)


class SendSingleMail(BaseModel):
    template_id: UUID
    subject_context: dict
    body_context: dict
    recipient: EmailStr


class Channel(str, Enum):
    EMAIL = 'EMAIL'
class PublicTemplate(BaseModel):
    template_id: UUID
    template_name: str
    channel_type: Channel
    version: str
    

class EmailTemplate(BaseModel):
    content: Jinja2Template
    subject: Jinja2Template
    version: str

class PublicCreateEmailTemplate(BaseModel):
    template_name: str
    channel_type: Channel
    template: EmailTemplate
    version: str

class CreateEmailTemplate(PublicCreateEmailTemplate):
    tenant_id: UUID


class TemplateInfoSchema(BaseModel):
    model_config = ConfigDict(
        extra='ignore'
    )
    id: UUID
    tenant_id: UUID
    subject: Jinja2Template
    body_content: Jinja2Template
    version: str
    body_context: list[str] | None
    subject_context: list[str] | None
    template_name: str


class TemplateSumary(BaseModel):
    id: UUID
    template_name: str