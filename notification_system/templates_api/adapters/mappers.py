from notification_system.common_utils.types.jinja2_pydantic_schema import (
    Jinja2Template
)
from ..models.template_model import TemplateDb as TemplateDB
from ..schemas.templates_schemas import (
    Channel,
    EmailTemplate,
    GenericTemplate,
    RegisterTemplate,
    SMSTemplate,
    Template,
    TemplateType,
)


def map_dto_to_orm(*, template_dto: RegisterTemplate) -> TemplateDB:
    data = {
        'template_name': template_dto.template_name,
        'channel': template_dto.channel_type,
        'version': template_dto.version,
        'tenant_id': template_dto.tenant_id,
    }
    context_keys_content = None
    context_keys_subject = None
    if isinstance(template_dto.template, EmailTemplate):
        if isinstance(template_dto.template.content, Jinja2Template):
            context_keys_content = list(
                template_dto.template.content.get_context_keys()
            )
        if isinstance(template_dto.template.subject, Jinja2Template):
            context_keys_subject = list(
                template_dto.template.subject.get_context_keys()
            )

    data['context_keys_content'] = context_keys_content
    data['context_keys_subject'] = context_keys_subject
    template_content = template_dto.template
    if isinstance(template_content, EmailTemplate):
        data['html_content'] = template_content.content
        data['subject'] = template_content.subject

    elif isinstance(template_content, SMSTemplate):
        data['sms_content'] = template_content.content
    elif isinstance(template_content, GenericTemplate):
        data['generic_title_content'] = template_content.title
        data['generic_content'] = template_content.content

    template_orm = TemplateDB(**data)
    return template_orm


def map_orm_to_dto(*, template_orm: TemplateDB) -> Template:
    """
    Cria uma instância do Pydantic Template a partir do modelo
    plano do SQLAlchemy.
    """
    template_data: TemplateType

    match template_orm.channel:
        case Channel.EMAIL:
            template_data = EmailTemplate(
                content=template_orm.html_content or '',
                subject=template_orm.subject or '',
                version=template_orm.version,
            )
        case Channel.SMS:
            template_data = SMSTemplate(
                content=template_orm.sms_content or '',
                version=template_orm.version,
            )
        case Channel.MOBILE_PUSH | Channel.WEB_PUSH | Channel.WEB_SOCKET:
            template_data = GenericTemplate(
                title=template_orm.generic_title_content,
                content=template_orm.generic_content or '',
                version=template_orm.version,
            )
        case _:
            raise ValueError(
                f'Canal não suportado para mapeamento: {template_orm.channel}'
            )

    return Template(
        id=template_orm.id,
        template_name=template_orm.template_name,
        channel_type=template_orm.channel,
        template=template_data,
        tenant_id=template_orm.tenant_id,
        version=template_orm.version,
        create_at=template_orm.created_at,
        updated_at=template_orm.updated_at,
        context_keys_content=template_orm.context_keys_content,
        context_keys_subject=template_orm.context_keys_subject,
    )
