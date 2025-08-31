from pydantic import BaseModel, EmailStr
from uuid import UUID
from typing import Any

class SingleEmailNotification(BaseModel):
    subject: str
    recipient: EmailStr
    template_id: UUID
    keys: dict[str, Any]
