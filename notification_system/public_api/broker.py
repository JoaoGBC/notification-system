from faststream.rabbit.fastapi import RabbitRouter
from pydantic import BaseModel, EmailStr
from uuid import UUID
from typing import Any

class SingleEmailNotification(BaseModel):
    recipient: EmailStr
    template_id: UUID
    body_keys: dict[str, Any]
    subject_keys: dict[str, Any]
    tenant_id: UUID



from .settings import settings

router = RabbitRouter(settings.BROKER_URL)
broker = router.broker
email_publisher = broker.publisher(
    'in-queue',
    title='Email-Notification-Publisher',
    description='Publisher para a fila de notificações transacionais via email',
    schema=SingleEmailNotification
    )
