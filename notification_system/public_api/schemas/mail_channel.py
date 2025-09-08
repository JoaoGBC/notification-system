from uuid import UUID
from pydantic import BaseModel, EmailStr
from enum import Enum


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
    