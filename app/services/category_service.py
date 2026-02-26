# app/services/category_service.py
from __future__ import annotations

from app import db
from app.models.category import Category


class CategoryService:
    def list_categories(self):
        return Category.query.order_by(Category.name).all()

    def get_category(self, category_id: int) -> Category:
        return Category.query.get_or_404(category_id)

    def create_category(self, form):
        name = (form.get("name") or "").strip()
        description = (form.get("description") or "").strip()

        data = {"name": name, "description": description}
        errors: list[str] = []

        if not name:
            errors.append("Name is required.")
        if len(name) > 60:
            errors.append("Name must be 60 characters or fewer.")
        if len(description) > 200:
            errors.append("Description must be 200 characters or fewer.")

        if errors:
            return None, errors, data

        cat = Category(name=name, description=description or None)
        db.session.add(cat)

        try:
            db.session.commit()
            return cat, [], data
        except Exception:
            db.session.rollback()
            return None, ["A category with that name already exists."], data

    def update_category(self, cat: Category, form):
        name = (form.get("name") or "").strip()
        description = (form.get("description") or "").strip()

        data = {"name": name, "description": description}
        errors: list[str] = []

        if not name:
            errors.append("Name is required.")
        if len(name) > 60:
            errors.append("Name must be 60 characters or fewer.")
        if len(description) > 200:
            errors.append("Description must be 200 characters or fewer.")

        if errors:
            return errors, data

        cat.name = name
        cat.description = description or None

        try:
            db.session.commit()
            return [], data
        except Exception:
            db.session.rollback()
            return ["A category with that name already exists."], data

    def delete_category(self, cat: Category) -> None:
        db.session.delete(cat)
        db.session.commit()