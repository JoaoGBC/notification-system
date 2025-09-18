from email.message import EmailMessage
from .mail_services import EmailService

async def send_mail_single(
        *,
        message_body: str,
        to: str,
        from_mail: str,
        subject: str,
        email_sender: EmailService
    ):
    message = EmailMessage()
    message["From"] = from_mail
    message["To"] = to
    message["Subject"] = subject
    message.set_content(message_body, subtype= "html")

    await email_sender.send_mail(
        message=message,
        sender=from_mail,
        recipients=to,
    )
