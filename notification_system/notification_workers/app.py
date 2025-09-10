from faststream import FastStream
from faststream.rabbit import RabbitBroker

from .schemas.message_schemas import SingleEmailNotification
from .services.template_services import get_template
from .services.mail_services import send_mail_single
from .settings import settings

broker = RabbitBroker(settings.BROKER_URL)
app = FastStream(broker=broker)


@broker.subscriber('in-queue')
async def handle_msg(message: SingleEmailNotification) -> None:
    template = await get_template(
        message.template_id,
        tenant_id=message.tenant_id
    )
    renderized_template = template.render_body(message.body_keys)
    renderized_subject = template.render_subject(message.subject_keys)
    await send_mail_single(
        message_body=renderized_template,
        to = message.recipient,
        from_mail="teste@meuzovo.com.br",
        subject=renderized_subject
    )



