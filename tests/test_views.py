from flask_injector import FlaskInjector
from injector import Binder, singleton
from unittest.mock import MagicMock

from app.repository import User, UserRepository


def test_route(app, client):
    def configure(binder: Binder):
        mock_repo = MagicMock(UserRepository)
        mock_user = MagicMock(User)
        mock_user.username = "Maria"
        mock_repo.get_by_name.return_value = mock_user

        binder.bind(UserRepository, to=mock_repo, scope=singleton)

    FlaskInjector(app=app, modules=[configure])

    response = client.get("/")

    assert b"Test: Username Maria" in response.data


def test_route_returns_user_not_found(app, client):
    def configure(binder: Binder):
        mock_repo = MagicMock(UserRepository)
        mock_repo.get_by_name.return_value = None

        binder.bind(UserRepository, to=mock_repo, scope=singleton)

    FlaskInjector(app=app, modules=[configure])

    response = client.get("/")
    assert b"User not found" in response.data
