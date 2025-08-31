from typing import Any

import jinja2
from jinja2 import meta
from pydantic import GetCoreSchemaHandler
from pydantic.json_schema import JsonSchemaValue
from pydantic_core import core_schema


class Jinja2Template(str):
    """
    Tipo customizado que representa uma string de um template jinja2 válida
    """

    @classmethod
    def __get_pydantic_core_schema__(  # noqa
        cls, source_type: Any, handler: GetCoreSchemaHandler
    ) -> core_schema.CoreSchema:
        def validate(
            v: str, handler: core_schema.ValidatorFunctionWrapHandler
        ) -> 'Jinja2Template':
            validated_str = handler(v)
            try:
                jinja2.Environment().parse(validated_str)
            except jinja2.exceptions.TemplateSyntaxError as e:
                raise ValueError(f'Sintaxe de template Jinja2 inválida: {e}')

            return cls(validated_str)

        string_schema = handler(str)

        return core_schema.no_info_wrap_validator_function(
            validate, string_schema
        )

    @classmethod
    def __get_pydantic_json_schema__(  # noqa
        cls, core_schema: core_schema.CoreSchema, handler: GetCoreSchemaHandler
    ) -> JsonSchemaValue:
        json_schema = handler(core_schema)

        json_schema.update(
            title='Template Jinja2',
            description='Uma string contendo um template'
            ' Jinja2 sintaticamente válido.',
            format='jinja2',
            examples=[
                '<h1>Olá, {{ nome }}!</h1>',
                'Seu pedido nº {{ pedido.id }} foi confirmado.',
            ],
        )
        return json_schema

    def get_context_keys(self) -> set[str]:
        env = jinja2.Environment()
        ast = env.parse(self)
        return meta.find_undeclared_variables(ast)
