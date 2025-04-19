from jinja2 import Template
import json
from recsys_arena.prompt_engine.parser import create_response_model


class PromptSpec:
    def __init__(self, name, template_str, schema_dict):
        self.name = name
        self.template = Template(template_str)
        self.schema_dict = schema_dict
        self.schema = create_response_model(schema_dict)

    def render(self, **kwargs) -> str:
        schema_instruction = self.build_schema_instruction()
        return self.template.render(schema_instruction=schema_instruction, **kwargs)

    def parse(self, raw_output: str):
        try:
            data = json.loads(raw_output)
            return self.schema(**data).dict()
        except Exception as e:
            return {"error": str(e)}

    def build_schema_instruction(self) -> str:
        formatted = ",\n  ".join(
            f'"{key}": "{value}"' for key, value in self.schema_dict.items()
        )
        return f"{{\n  {formatted}\n}}"
