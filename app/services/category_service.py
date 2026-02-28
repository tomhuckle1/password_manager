from __future__ import annotations

from sqlalchemy.exc import IntegrityError

from app.models.category import Category
from app.repositories.category_repository import CategoryRepository
from app.utils.validators import validate_category_form


class CategoryService:
    def __init__(self, categories: CategoryRepository):
        self.categories = categories

    def list_categories(self):
        return self.categories.list_ordered()

    def get_category(self, category_id: int) -> Category:
        return self.categories.get(category_id)

    def create_category(self, form):
        # Validate
        data, errors = validate_category_form(
            name=form.get("name"),
            description=form.get("description"),
        )
        if errors:
            return None, errors, data

        cat = Category(
            name=data["name"],
            description=data["description"],
        )

        try:
            self.categories.add(cat)
            return cat, [], data
        except IntegrityError:
            return None, ["A category with that name already exists."], data

    def update_category(self, cat: Category, form):
        # Validate
        data, errors = validate_category_form(
            name=form.get("name"),
            description=form.get("description"),
        )
        if errors:
            return errors, data

        cat.name = data["name"]
        cat.description = data["description"]

        try:
            self.categories.commit()
            return [], data
        except IntegrityError:
            return ["A category with that name already exists."], data

    def can_delete_category(self, cat: Category) -> bool:
        # returns true if no passwords associated with category
        return not self.categories.has_password_entries(cat)

    def delete_category(self, cat: Category) -> None:
        self.categories.delete(cat)