from __future__ import annotations

from sqlalchemy.exc import IntegrityError

from app.models.category import Category
from app.repositories.category_repository import CategoryRepository


class CategoryService:
    def __init__(self, categories: CategoryRepository):
        self.categories = categories

    def list_categories(self):
        return self.categories.list_ordered()

    def get_category(self, category_id: int) -> Category:
        return self.categories.get(category_id)

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

        try:
            self.categories.add(cat)
            return cat, [], data
        except IntegrityError:
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
            self.categories.commit()
            return [], data
        except IntegrityError:
            return ["A category with that name already exists."], data

    def delete_category(self, cat: Category) -> None:
        self.categories.delete(cat)