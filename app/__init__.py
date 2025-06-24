import os

from flask_injector import FlaskInjector, singleton
import flask_injector
from flask_sqlalchemy import SQLAlchemy
from injector import Injector, Module
import yaml
from flask import Flask

from app.db import db
from app.repository import User, UserRepository
from app.views import people


class AppModule(Module):
    def __init__(self, app):
        self.app = app

    """Configure the application."""

    def configure(self, binder):
        # We configure the DB here, explicitly, as Flask-SQLAlchemy requires
        # the DB to be configured before request handlers are called.
        db = self.configure_db(self.app)
        binder.bind(SQLAlchemy, to=db, scope=singleton)
        binder.bind(UserRepository, to=UserRepository(db), scope=singleton)

    def configure_db(self, app):
        db.create_all()
        user = User()
        if not User.query.filter_by(username="Tom").first():
            user.username = "Tom"
            db.session.add(user)
            db.session.commit()
        return db


def create_app():
    app = Flask(__name__)
    config = os.path.join(os.getcwd(), "config.yml")
    app.config.from_file(config, yaml.safe_load)

    db.init_app(app)

    app.register_blueprint(people, url_prefix="")

    with app.app_context():
        injector = Injector([AppModule(app)])

    FlaskInjector(app=app, injector=injector)

    return app
