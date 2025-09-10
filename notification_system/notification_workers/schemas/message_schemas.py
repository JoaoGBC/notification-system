from typing import Any
from uuid import UUID

from pydantic import BaseModel, EmailStr


class SingleEmailNotification(BaseModel):
    recipient: EmailStr
    template_id: UUID
    tenant_id: UUID
    body_keys: dict[str, Any]
    subject_keys: dict[str, Any]
