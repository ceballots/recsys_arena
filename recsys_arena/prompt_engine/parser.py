from pydantic import create_model


def create_response_model(schema: dict):
    fields = {k: (str, ...) for k in schema}
    return create_model("DynamicResponse", **fields)
