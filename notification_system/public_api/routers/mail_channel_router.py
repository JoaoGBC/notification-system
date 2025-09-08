from http import HTTPStatus
from typing import Annotated
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException

from ..security import PublicFacingKeycloakToken, RoleChecker
from ..services.mail_services import get_template
from ..schemas.mail_channel import SendSingleMail

mail_channel_router = APIRouter(
    prefix= '/mail',
    tags=['Mail']
)


T_send_role = Annotated[
    PublicFacingKeycloakToken, 
    Depends(RoleChecker(required_roles=['notifications:send']))
    ]

T_get_template_role = Annotated[
    PublicFacingKeycloakToken,
    Depends(RoleChecker(required_roles=['notifications:read-template']))
]


@mail_channel_router.post('/send')
async def send_mail_view(user: T_send_role, send_mail_request: SendSingleMail):
    template = await get_template(
        template_id= send_mail_request.template_id,
        tenant_id= user['tenant_id']
    )

    if not template:
        raise HTTPException(
            status_code= HTTPStatus.NOT_FOUND,
            detail='Template not found',
        )
    ...



@mail_channel_router.get('/')
async def get_template_view(template_id: UUID, user: T_get_template_role):
    template = await get_template(template_id= template_id, tenant_id=user['tenant_id'])
    return template