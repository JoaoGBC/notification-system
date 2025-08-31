


from uuid import UUID
import httpx

from ..schemas.email_template_schemas import EmailTemplate


async def get_template(template_id: UUID) -> EmailTemplate:
    try: 
        async with httpx.AsyncClient() as client:
            response = (await client.get(
                url='http://localhost:8000/templates/', 
                params={
                    'template_id': template_id,
                }
            )).raise_for_status()
            response = response.json()
            return EmailTemplate(
                    template_body= response['template']['content'],
                    subject= response['template']['subject'],
                    body_context_keys= response['context_keys_content'],
                    subject_context_keys= response['context_keys_subject']
                )
    except httpx.HTTPStatusError as e:
        #Tratar os erros/status previstos na api de templates aqui
        pass
