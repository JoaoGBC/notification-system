from http import HTTPStatus
from typing import Annotated
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException

from ..security import PublicFacingKeycloakToken, RoleChecker
from ..services.utils.mail_template_api_handler import get_template, list_templates, create_template
from ..schemas.mail_channel import PublicCreateEmailTemplate, CreateEmailTemplate, SendSingleMail, TemplateInfoSchema
from ..broker import broker, SingleEmailNotification




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


T_create_template_role = Annotated[
    PublicFacingKeycloakToken,
    Depends(RoleChecker(required_roles=['notifications:create-template']))
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
    

    if (
        template.body_context != [*send_mail_request.body_context]
        or
        template.subject_context != [*send_mail_request.subject_context]
        ):
        raise HTTPException(
            status_code= HTTPStatus.BAD_REQUEST,
            detail = 'Registered template context and given request dont match'
        )
    
    a = await broker.publish(
        message=SingleEmailNotification(
            recipient=send_mail_request.recipient,
            template_id=send_mail_request.template_id,
            body_keys=send_mail_request.body_context,
            subject_keys=send_mail_request.subject_context,
            tenant_id=user['tenant_id']
        ),
        queue='in-queue'
    )



@mail_channel_router.get('/{template_id}')
async def get_template_view(template_id: UUID, user: T_get_template_role):
    template = await get_template(template_id= template_id, tenant_id=user['tenant_id'])
    return template



@mail_channel_router.get('/')
async def list_template_view(user: T_get_template_role):
    template = await list_templates(tenant_id=user['tenant_id'])
    return template




@mail_channel_router.post(
        '/',
        response_model= TemplateInfoSchema,
    )
async def create_template_view(
        user: T_get_template_role,
        template: PublicCreateEmailTemplate,
    ):
        template = CreateEmailTemplate(
            **template.model_dump(),
            tenant_id= user['tenant_id']
        )
        
        created_template = await create_template(
            template=template
        )

        return created_template