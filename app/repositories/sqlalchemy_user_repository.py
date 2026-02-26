from __future__ import annotations
from typing import Optional
from flask_sqlalchemy import SQLAlchemy
from app.models.user import User
from app.repositories.user_repository import UserRepository


class SqlAlchemyUserRepository(UserRepository):
    def __init__(self, db: SQLAlchemy):
        self.db = db

    def get_by_email(self, email: str) -> Optional[User]:
        return User.query.filter_by(email=email).first()

    def get_by_id(self, user_id: int) -> Optional[User]:
        return self.db.session.get(User, user_id)

    def add(self, user: User) -> None:
        self.db.session.add(user)
        self.db.session.commit()