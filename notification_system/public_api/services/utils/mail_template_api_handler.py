from uuid import UUID
import httpx
from httpx_auth import OAuth2ClientCredentials

from ...settings import settings
from .template_schema import TemplateInfoSchema, TemplateSumary


credentials = OAuth2ClientCredentials(
    token_url= f'{settings.KEYCLOAK_SERVER_URL}/realms/'
               f'{settings.KEYCLOAK_REALM}/protocol/openid-connect/token',
    client_id= settings.KEYCLOAK_CLIENT_ID,
    client_secret= settings.KEYCLOAK_CLIENT_SECRET,
)
        



template_api_client = httpx.AsyncClient(
    auth=credentials,
    base_url='http://localhost:8000'
)



def __get_template_api_response_mapper(
        api_response: dict
    ) -> TemplateInfoSchema: 
    try:
        return TemplateInfoSchema(
            id = api_response.get('id'),
            tenant_id= api_response.get('tenant_id'),
            subject = api_response.get('template').get('subject'),
            body_content = api_response.get('template').get('content'),
            version= api_response.get('template').get('version'),
            body_context= api_response.get('context_keys_content', None),
            subject_context= api_response.get('context_keys_subject', None),
            template_name= api_response.get('template_name')
        )
    except KeyError:
        raise ValueError('Invalid response object from templates_api call')



def __list_template_api_response_mapper(
        api_response: dict
    ) -> TemplateSumary: 
    try:
        return TemplateSumary(
            id = api_response.get('id'),
            template_name= api_response.get('template_name')
        )
    except KeyError:
        raise ValueError('Invalid response object from templates_api call')


async def get_template(
        *,
        template_id: UUID,
        tenant_id: UUID
    ) -> TemplateInfoSchema:
    try:
        template = (await template_api_client.get(
            url=f'/templates/{tenant_id}/{template_id}',
        )).raise_for_status()
        return __get_template_api_response_mapper(template.json())
    except Exception as e:
        raise e
    

async def list_templates(
        *,
        tenant_id: UUID,
    ):
    try:
        template_list = (
            await template_api_client.get(
                url = f'/templates/{tenant_id}',
            )
        ).raise_for_status()
        return (
            __list_template_api_response_mapper(template_item) 
            for template_item in template_list.json().get('templates')
        )
    except Exception as e:
        raise e