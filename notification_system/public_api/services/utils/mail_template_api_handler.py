from uuid import UUID
import httpx
from httpx_auth import OAuth2ClientCredentials

from ...settings import settings



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



async def get_template(
        *,
        template_id: UUID,
        tenant_id: UUID
    ):
    try:
        template = (await template_api_client.get(
            url='/templates/',
            params={
                'template_id' : template_id,
                'tenant_id' : tenant_id,
            }
        )).raise_for_status()
        return template.json()
    except Exception as e:
        raise e

    ...