from jinja2 import Environment
from pydantic import BaseModel


class EmailTemplate(BaseModel):
    template_body: str
    subject: str
    body_context_keys: list[str] | None
    subject_context_keys: list[str] | None

    def __render_template(self, template_str: str, context: dict) -> str:
        env = Environment()
        unrenderized_template = env.from_string(template_str)
        renderized_template = unrenderized_template.render(context)

        return renderized_template

    def render_body(self, context: dict) -> str:
        return self.__render_template(self.template_body, context)
        
    def render_subject(self, context: dict) -> str:
        return self.__render_template(self.subject, context)