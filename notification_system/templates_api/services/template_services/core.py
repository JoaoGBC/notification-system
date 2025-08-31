from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from uuid import UUID

from notification_system.templates_api.schemas.templates_schemas import RegisterTemplate, Template
from notification_system.templates_api.models.template_model import Channel, TemplateDb
from .exceptions import InvalidDbRecord, TemplateIntegrityError, TemplateNotFound
from ...adapters.mappers import map_dto_to_orm, map_orm_to_dto




async def register_template(
        *,
        template: RegisterTemplate,
        session: AsyncSession
    ) -> bool:
    """
    check rules and persists a template on DB
    returns true e the template has been sucessfuly saved
    """
    template_db = await session.scalar(
        select(
            TemplateDb
        ).filter(
            TemplateDb.template_name == template.template_name,
            TemplateDb.tenant_id == template.tenant_id
        )
    )

    if template_db:
        raise TemplateIntegrityError
    
    try:
        template_db = map_dto_to_orm(template_dto=template)
        session.add(template_db)
        await session.commit()
        await session.refresh(template_db)
        return map_orm_to_dto(template_orm=template_db)
    except Exception as e:
        return False



async def get_template(
        *,
        template_id: UUID,
        session: AsyncSession
    ) -> Template:
    template_db = await session.scalar(
        select(TemplateDb).where(TemplateDb.id == template_id)
    )

    if not template_db:
        raise TemplateNotFound
    

    try:
        template_dto = map_orm_to_dto(template_orm=template_db)
    except Exception as e:
        raise InvalidDbRecord
    
    return template_dto


async def list_templates_by_tenant(
        *,
        tenant_id: UUID,
        session: AsyncSession,    
    ) -> list[tuple[UUID, str, Channel]]:

    ids = (await session.execute(
        select(TemplateDb.id,  TemplateDb.template_name, TemplateDb.channel)
        .where(TemplateDb.tenant_id == tenant_id)
    )).all()
    return ids



async def delete_templates(
        *,
        template_id: UUID,
        session: AsyncSession
    ) -> None:

    template_db = await session.scalar(
        select(TemplateDb)
        .where(TemplateDb.id == template_id)
    )

    if not template_db:
        raise TemplateNotFound
    
    try:
        await session.delete(template_db)
        await session.commit()
    except Exception as e:
        await session.rollback()
        raise e
    