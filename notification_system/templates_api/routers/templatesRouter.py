from http import HTTPStatus
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession



from ..database import get_async_session
from ..schemas.templates_schemas import RegisterTemplate, Template, TemplateSumaryList
from ..services import (
    register_template,
    get_template,
    list_templates_by_tenant,
    delete_templates,
    TemplateNotFound,
    InvalidDbRecord
)

templates_router = APIRouter(prefix='/templates', tags=['templates'])

T_session = Annotated[AsyncSession, Depends(get_async_session)]

@templates_router.post(
    '/', 
    response_model = Template,
    status_code= HTTPStatus.CREATED
)
async def create_template(
    template: RegisterTemplate,
    session: T_session
):

    resp = await register_template(
        template=template,
        session=session
    )
    return resp


@templates_router.get(
    '/', 
    response_model = Template,
    status_code= HTTPStatus.OK
)
async def get_template_by_uuid(
    template_id: UUID,
    session: T_session
):
    try:
        resp = await get_template(
            template_id=template_id,
            session=session
        )
    except TemplateNotFound:
        raise HTTPException(
            detail= 'Template not found',
            status_code= HTTPStatus.NOT_FOUND
        )
    except InvalidDbRecord:
        raise HTTPException(
            detail= 'Corrupted template. Update or delete record and try again',
            status_code= HTTPStatus.INTERNAL_SERVER_ERROR
        )
    return resp
    



@templates_router.get(
    '/list', 
    response_model =  TemplateSumaryList | list[None],
    status_code= HTTPStatus.OK
)
async def list_templates_tenant(
        tenant_id: UUID,
        session: T_session,
    ):
    try:
        summaries = await list_templates_by_tenant(
            session=session,
            tenant_id= tenant_id,
        )
        summaries = [
            {
                'id' : item[0],
                'template_name' : item[1],
                'channel' : item[2]
            } 
            for item in summaries
        ]
        return {'templates' : summaries} 

    except Exception as e:
        raise e


@templates_router.delete(
    '/',
    status_code= HTTPStatus.ACCEPTED,
)
async def delete(
        template_id: UUID,
        session: T_session,
    ):
    try:
        await delete_templates(
            template_id=template_id,
            session=session
        )
        return {}
    except TemplateNotFound as e:
        raise HTTPException(
            status_code= HTTPStatus.NOT_FOUND,
            detail= 'Template not found'
        )
    except Exception as e:
        raise HTTPException(
            detail= "Operation failed",
            status_code= HTTPStatus.INTERNAL_SERVER_ERROR
        )