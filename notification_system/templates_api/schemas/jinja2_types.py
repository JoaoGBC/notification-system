from typing import Any
import jinja2
from jinja2 import meta
from pydantic import GetCoreSchemaHandler
from pydantic_core import core_schema
from pydantic.json_schema import JsonSchemaValue

class Jinja2Template(str):
    """
    Tipo customizado que representa uma string de um template jinja2 válida
    """

    @classmethod
    def __get_pydantic_core_schema__(
        cls, source_type: Any, handler: GetCoreSchemaHandler
    ) -> core_schema.CoreSchema:
        

        def validate(v: str, handler: core_schema.ValidatorFunctionWrapHandler) -> 'Jinja2Template':
            validated_str = handler(v)
            try:
                jinja2.Environment().parse(validated_str)
            except jinja2.exceptions.TemplateSyntaxError as e:
                raise ValueError(f'Sintaxe de template Jinja2 inválida: {e}')
            
            return cls(validated_str)
        
        
        string_schema = handler(str)
        
        return core_schema.no_info_wrap_validator_function(validate, string_schema)
    

    @classmethod
    def __get_pydantic_json_schema__(
        cls, core_schema: core_schema.CoreSchema, handler: GetCoreSchemaHandler
    ) -> JsonSchemaValue:
        # 1. Primeiro, obtemos o esquema JSON base que o Pydantic geraria.
        #    Para a nossa classe, será um simples schema de string.
        json_schema = handler(core_schema)
        
        # 2. Agora, modificamos esse dicionário para adicionar nossos metadados.
        json_schema.update(
            title='Template Jinja2',
            description='Uma string contendo um template Jinja2 sintaticamente válido.',
            format='jinja2',  # Um formato customizado para maior clareza
            examples=[      # Adicionamos exemplos úteis
                '<h1>Olá, {{ nome }}!</h1>',
                'Seu pedido nº {{ pedido.id }} foi confirmado.',
            ],
        )
        return json_schema
    
    def get_context_keys(self) -> set[str]:
        env = jinja2.Environment()
        ast = env.parse(self)
        return meta.find_undeclared_variables(ast)