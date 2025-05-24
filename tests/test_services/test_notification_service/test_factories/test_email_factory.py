import pytest
from app.services.notification.factories import EmailBuilderFactory
from app.services.notification.factories import IBuilderFactory
from app.services.notification.builders import IBuilder

def test_create_email_builder_factory():
    factory = EmailBuilderFactory()
    assert factory is not None
    assert isinstance(factory, EmailBuilderFactory)
    assert isinstance(factory, IBuilderFactory)
    assert factory.create_builder("login") is not None
    assert isinstance(factory.create_builder("login"), IBuilder)
    assert factory.create_builder("reminder") is not None
    assert isinstance(factory.create_builder("reminder"), IBuilder)

def test_create_email_builder_factory_invalid_type():
    factory = EmailBuilderFactory()
    with pytest.raises(ValueError) as excinfo:
        factory.create_builder("invalid_type")
    assert str(excinfo.value) == "Builder no soportado"

    