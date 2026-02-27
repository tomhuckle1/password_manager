from __future__ import annotations

from flask_sqlalchemy import SQLAlchemy

from app.models.password import PasswordEntry
from app.repositories.password_repository import PasswordRepository


class SqlAlchemyPasswordRepository(PasswordRepository):
    def __init__(self, db: SQLAlchemy):
        self.db = db

    def get_or_404(self, entry_id: int) -> PasswordEntry:
        return PasswordEntry.query.get_or_404(entry_id)

    def add(self, entry: PasswordEntry) -> None:
        self.db.session.add(entry)
        self.db.session.commit()

    def commit(self) -> None:
        self.db.session.commit()

    def delete(self, entry: PasswordEntry) -> None:
        self.db.session.delete(entry)
        self.db.session.commit()