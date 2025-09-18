from uuid import UUID

import httpx

from ..schemas.email_template_schemas import EmailTemplate
from ..settings import settings


async def get_template(
        *,
        template_id: UUID,
        tenant_id: UUID
    ) -> EmailTemplate:
    try:
        async with httpx.AsyncClient() as client:
            response = (
                await client.get(
                    url=f'{settings.TEMPLATE_API_HOST}/{tenant_id}/{template_id}',
                )
            ).raise_for_status()
            response = response.json()
            return EmailTemplate(
                template_body=response['template']['content'],
                subject=response['template']['subject'],
                body_context_keys=response['context_keys_content'],
                subject_context_keys=response['context_keys_subject'],
            )
    except httpx.HTTPStatusError:
        # Tratar os erros/status previstos na api de templates aqui
        pass
