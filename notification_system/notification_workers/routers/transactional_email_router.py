from faststream import Context
from faststream.rabbit import RabbitRouter

from ..schemas.message_schemas import SingleEmailNotification
from ..services.mail_services import EmailService
from ..services.template_services import get_template
from ..services.notification_services import send_mail_single

transational_email_router = RabbitRouter()

@transational_email_router.subscriber("in-queue")
async def send_transactional_email_notification(
        message: SingleEmailNotification, 
        context = Context()
    ) -> None:
    
    email_sender: EmailService = context.get('email_service_instance')
    template = await get_template(
        template_id=message.template_id,
        tenant_id=message.tenant_id
    )
    renderized_template = template.render_body(message.body_keys)
    renderized_subject = template.render_subject(message.subject_keys)
    
    await send_mail_single(
        message_body=renderized_template,
        to = message.recipient,
        from_mail="teste@meuzovo.com.br",
        subject=renderized_subject,
        email_sender=email_sender
    )