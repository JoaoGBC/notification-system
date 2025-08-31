from typing import Any
from uuid import UUID

from pydantic import BaseModel, EmailStr


class SingleEmailNotification(BaseModel):
    subject: str
    recipient: EmailStr
    template_id: UUID
    keys: dict[str, Any]
