from contextlib import asynccontextmanager
from faststream import Context, ContextRepo, FastStream
from faststream.rabbit import RabbitBroker


from .services.mail_services import EmailService
from .settings import settings

from .routers.transactional_email_router import transational_email_router
broker = RabbitBroker(settings.BROKER_URL)







broker.include_router(transational_email_router)



@asynccontextmanager
async def lifespan(context: ContextRepo):
    email_service_instance = EmailService(
        hostname = settings.SMTP_HOST,
        port = settings.SMTP_PORT,
        username= settings.SMTP_USERNAME,
        password=settings.SMTP_PASSWORD,
        use_tls=False,
        max_connections=settings.MAX_SMTP_CONNECTIONS,
    )
    await email_service_instance.connect()
    context.set_global('email_service_instance', email_service_instance)
    yield

    email_service_instance_from_context = context.get('email_service_instance')
    if email_service_instance_from_context:
        await email_service_instance.disconnect()

app = FastStream(broker=broker, lifespan=lifespan)


