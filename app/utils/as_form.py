import inspect

from fastapi import Form
from pydantic import BaseModel, ValidationError

from app.exceptions.api import InvalidFormData


def as_form(cls: type[BaseModel]):
    new_parameters = []

    for field_name, model_field in cls.model_fields.items():
        new_parameters.append(
            inspect.Parameter(
                field_name,
                inspect.Parameter.POSITIONAL_ONLY,
                default=Form(model_field.default[0] if isinstance(model_field.default, tuple) else model_field.default)
                if not model_field.is_required()
                else Form(),
                annotation=model_field.annotation,
            )
        )

    async def as_form_func(**data):
        try:
            return cls(**data)
        except ValidationError as ex:
            raise InvalidFormData(details={"errors": ex.errors()}) from ex

    sig = inspect.signature(as_form_func)
    sig = sig.replace(parameters=new_parameters)
    as_form_func.__signature__ = sig
    cls.as_form = as_form_func
    return cls
