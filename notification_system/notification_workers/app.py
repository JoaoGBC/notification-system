from typing import Any
from uuid import UUID
from faststream import FastStream
from faststream.rabbit import RabbitBroker

from .settings import settings 
from .services.template_services import get_template

broker = RabbitBroker(settings.BROKER_URL)
app = FastStream(broker=broker)


from pydantic import BaseModel, EmailStr



class SingleEmailNotification(BaseModel):
    subject: str
    recipient: EmailStr
    template_id: UUID
    keys: dict[str, Any]


@broker.subscriber("in-queue")
async def handle_msg(message: SingleEmailNotification) -> None:
    template = await get_template(message.template_id)
    print(f' template: {template}')