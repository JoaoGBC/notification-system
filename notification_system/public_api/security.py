from http import HTTPStatus
from uuid import UUID
from fastapi import Depends, HTTPException, Request
from typing import Optional
import jwt
from typing import TypedDict
from .settings import settings

from fastapi.security import OAuth2
from fastapi.openapi.models import OAuthFlows, OAuthFlowClientCredentials
from fastapi.security.utils import get_authorization_scheme_param

class Oauth2ClientCredentials(OAuth2):
    def __init__(
        self,
        token_url: str,
        scheme_name: str = None,
        scopes: dict = None,
        auto_error: bool = True,
    ):
        if not scopes:
            scopes = {}
        flows = OAuthFlows(
            clientCredentials=OAuthFlowClientCredentials(
                tokenUrl=token_url,
                scopes=scopes
            )
        )
        super().__init__(flows=flows, scheme_name=scheme_name, auto_error=auto_error)

    async def __call__(self, request: Request) -> Optional[str]:
        # Esta parte extrai o token "Bearer" do cabeçalho, similar ao HTTPBearer
        authorization: str = request.headers.get("Authorization")
        scheme, param = get_authorization_scheme_param(authorization)
        if not authorization or scheme.lower() != "bearer":
            if self.auto_error:
                raise HTTPException(
                    status_code=HTTPStatus.UNAUTHORIZED,
                    detail="Not authenticated",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            else:
                return None
        return param


oauth2_scheme = Oauth2ClientCredentials(
    token_url=f'{settings.KEYCLOAK_SERVER_URL}/realms/{settings.KEYCLOAK_REALM}/protocol/openid-connect/token'
)

jwks_client = jwt.PyJWKClient(f'{settings.KEYCLOAK_SERVER_URL}/realms/{settings.KEYCLOAK_REALM}/protocol/openid-connect/certs')


class PublicFacingKeycloakToken(TypedDict):
    exp : str
    iat : str
    jti : str
    iss : str
    aud : list[str]
    sub : UUID
    type : str
    azp : str
    acr : str
    allowed_origins : list[str]
    realm_access : dict[str : str | list[str]]
    resourse_access : dict[str : str | list[str]]
    account : dict
    scope : str
    tenant_id : UUID
    clientHost : str
    email_verified: bool
    preferred_username : str
    clientAddress : str
    client_id : str



async def get_current_user(
        token: str = Depends(oauth2_scheme)
    ) -> PublicFacingKeycloakToken:
    try:
        public_signing_key = jwks_client.get_signing_key_from_jwt(
            token = token,
        )

        payload = jwt.decode(
            jwt=token,
            key=public_signing_key.key,
            algorithms=['RS256'],
            audience=settings.KEYCLOAK_CLIENT_ID,
        )

        tenant_id = payload.get('tenant_id')
        if not tenant_id:
            raise HTTPException(
                status_code= HTTPStatus.UNAUTHORIZED,
                detail='Invalid token: tenant not found'
            )
        
        return payload
    
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail='Expired Token',
            headers={'WWW-Authenticate': 'Bearer'},
        )
    except jwt.InvalidTokenError as e:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail=f'Invalid token: {e}',
            headers={'WWW-Authenticate': 'Bearer'},
        )
    


class RoleChecker:
    def __init__(self, required_roles: list[str]):
        self.required_roles = required_roles
    

    def __call__(
            self,
            current_user: dict = Depends(get_current_user)
        ) -> PublicFacingKeycloakToken:
        try:
            resource_access = current_user.get('resource_access', {})

            user_roles = resource_access.get(
                settings.KEYCLOAK_CLIENT_ID, {}
            ).get(
                'roles', []
            )
            if not any([role in user_roles for role in self.required_roles]):
                raise HTTPException(
                    status_code=HTTPStatus.FORBIDDEN,
                    detail='This resourse require at least'
                    f' one of the roles: [{self.required_roles}]'
                )
            return current_user
        except HTTPException as e:
            raise e
        except Exception:
            raise HTTPException(
                status_code=HTTPStatus.FORBIDDEN,
                detail='It was impossible to verify the access roles'
            )
