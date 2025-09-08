import aiosmtplib
from email.message import EmailMessage

async def send_mail_single(
        *,
        message_body: str,
        to: str,
        from_mail: str,
        subject: str
    ):
    message = EmailMessage()
    message["From"] = from_mail
    message["To"] = to
    message["Subject"] = subject
    message.set_content(message_body, subtype= "html")

    await aiosmtplib.send(
        message,
        hostname="127.0.0.1",
        port = 1025
    )