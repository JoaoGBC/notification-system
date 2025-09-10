from uuid import UUID
from pydantic import BaseModel, ConfigDict

from notification_system.common_utils.types.jinja2_pydantic_schema import Jinja2Template


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


