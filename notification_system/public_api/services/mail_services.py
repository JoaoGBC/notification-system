from uuid import UUID
from email_validator import validate_email
from httpx import AsyncClient


from .utils.mail_template_api_handler import get_template

async def publish_mail_notifation_event(
        *,
        tenant_id: UUID,
        template_id: UUID,
        body_context: dict,
        subject_context: dict,
        recipient: str,  
    ):
    template = await get_template(
        template_id=template_id,
        tenant_id=tenant_id
    )
    return template 