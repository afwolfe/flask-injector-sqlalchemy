import os

from flask_injector import singleton
import flask_injector
from flask_sqlalchemy import SQLAlchemy
import yaml
from flask import Flask

from app.db import db
from app.repository import User, UserRepository
from app.views import people


def setup_database(app):
    with app.app_context():
        db.create_all()
        user = User()
        if not User.query.filter_by(username="Tom").first():
            user.username = "Tom"
            db.session.add(user)
            db.session.commit()


def configure(binder):
    binder.bind(SQLAlchemy, to=db, scope=singleton)
    binder.bind(UserRepository, to=UserRepository(db), scope=singleton)


def create_app():
    app = Flask(__name__)
    config = os.path.join(os.getcwd(), "config.yml")
    app.config.from_file(config, yaml.safe_load)

    db.init_app(app)

    app.register_blueprint(people, url_prefix="")

    flask_injector.FlaskInjector(app=app, modules=[configure])

    setup_database(app)
    return app
