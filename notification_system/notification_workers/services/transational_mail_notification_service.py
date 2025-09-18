from typing import Any
from uuid import UUID

from .template_services import get_template

async def send_transational_notification(
        template_id: UUID,
        tenant_id: UUID,
        body_context: dict[str, Any],
        subject_context: dict[str, Any],
        recipient: str,
    ):
        template = await get_template(
            template_id=template_id,
            tenant_id=tenant_id,
        )

        renderized_body = template.render_body(
            context = body_context
        )

        renderized_subject = template.render_subject(
                context=subject_context,
        )

        
    