from uuid import UUID
from pydantic import BaseModel, ConfigDict


class TemplateInfoSchema(BaseModel):
    model_config = ConfigDict(
        extra='ignore'
    )
    id: UUID
    tenant_id: UUID
    body_context: list[str] | None
    subject_context: list[str] | None
