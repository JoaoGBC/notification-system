from typing import Any
from uuid import UUID
from faststream import FastStream
from faststream.rabbit import RabbitBroker

from .settings import settings 
from .services.template_services import get_template
from .schemas.message_schemas import SingleEmailNotification

broker = RabbitBroker(settings.BROKER_URL)
app = FastStream(broker=broker)







@broker.subscriber("in-queue")
async def handle_msg(message: SingleEmailNotification) -> None:
    template = await get_template(message.template_id)
    renderized_template = template.render_body(message.keys)

    print(renderized_template)
    