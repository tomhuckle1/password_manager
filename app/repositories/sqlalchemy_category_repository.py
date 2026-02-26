from __future__ import annotations

from typing import List
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError

from app.models.category import Category
from app.repositories.category_repository import CategoryRepository


class SqlAlchemyCategoryRepository(CategoryRepository):
    def __init__(self, db: SQLAlchemy):
        self.db = db

    def list_ordered(self) -> List[Category]:
        return Category.query.order_by(Category.name).all()

    def get(self, category_id: int) -> Category:
        return Category.query.get_or_404(category_id)

    def add(self, category: Category) -> None:
        self.db.session.add(category)
        try:
            self.db.session.commit()
        except IntegrityError:
            self.db.session.rollback()
            raise

    def commit(self) -> None:
        try:
            self.db.session.commit()
        except IntegrityError:
            self.db.session.rollback()
            raise

    def delete(self, category: Category) -> None:
        self.db.session.delete(category)
        try:
            self.db.session.commit()
        except IntegrityError:
            self.db.session.rollback()
            raise

    def has_password_entries(self, category: Category) -> bool:
        return bool(category.password_entries) and len(category.password_entries) > 0