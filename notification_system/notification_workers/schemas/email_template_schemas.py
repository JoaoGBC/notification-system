from jinja2 import Environment
from pydantic import BaseModel


class EmailTemplate(BaseModel):
    template_body: str
    subject: str
    body_context_keys: list[str] | None
    subject_context_keys: list[str] | None

    def render_body(self, context: dict) -> str:
        env = Environment()
        unrenderized_template = env.from_string(self.template_body)
        renderized_template = unrenderized_template.render(context)

        return renderized_template
