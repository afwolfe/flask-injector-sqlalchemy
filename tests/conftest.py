from flask import Flask
from flask_injector import FlaskInjector
import pytest
from injector import Binder, singleton
from unittest.mock import MagicMock


from app import create_app
from app.repository import User, UserRepository


def configure(binder: Binder):
    mock_repo = MagicMock(UserRepository)
    mock_user = MagicMock(User)
    mock_user.username = "Tom"
    mock_repo.get_by_name.return_value = mock_user

    binder.bind(UserRepository, to=mock_repo, scope=singleton)


@pytest.fixture
def app():
    app = create_app()
    FlaskInjector(app=app, modules=[configure])

    yield app


@pytest.fixture
def client(app: Flask):
    yield app.test_client()
