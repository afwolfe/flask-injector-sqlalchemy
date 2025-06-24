from typing import Optional
from flask_sqlalchemy import SQLAlchemy
from injector import inject

from app.db import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)


class UserRepository:
    @inject
    def __init__(self, db: SQLAlchemy):
        self.db = db

    def get_all(self):
        db.query(User).all()

    def get_by_name(self, name: str) -> Optional[User]:
        return self.db.session.query(User).filter_by(username=name).first()
