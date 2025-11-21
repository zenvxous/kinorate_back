import pytest
from pydantic import BaseModel

from app.exceptions.api import InvalidFormData
from app.utils.as_form import as_form


@as_form
class FormModel(BaseModel):
    name: str
    age: int
    email: str | None = None


class TestAsForm:
    @pytest.mark.unit
    def test_as_form_decorator(self):
        assert hasattr(FormModel, 'as_form')
        assert callable(FormModel.as_form)

    @pytest.mark.unit
    async def test_as_form_valid_data(self):
        form_data = await FormModel.as_form(
            name="John",
            age=25,
            email="john@example.com"
        )
        assert isinstance(form_data, FormModel)
        assert form_data.name == "John"
        assert form_data.age == 25
        assert form_data.email == "john@example.com"

    @pytest.mark.unit
    async def test_as_form_with_optional_field(self):
        form_data = await FormModel.as_form(
            name="Jane",
            age=30
        )
        assert isinstance(form_data, FormModel)
        assert form_data.name == "Jane"
        assert form_data.age == 30
        assert form_data.email is None

    @pytest.mark.unit
    async def test_as_form_invalid_data(self):
        with pytest.raises(InvalidFormData):
            await FormModel.as_form(
                name="John",
                age="not_a_number"
            )

