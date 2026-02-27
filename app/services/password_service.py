from __future__ import annotations

from app import db
from app.models.category import Category
from app.models.password import PasswordEntry


class PasswordService:
    def list_categories(self):
        return Category.query.order_by(Category.name).all()

    def get_entry_or_404(self, entry_id: int) -> PasswordEntry:
        return PasswordEntry.query.get_or_404(entry_id)

    def create_password_entry(self, form, *, user_id: int):
        name = (form.get("name") or "").strip()
        website = (form.get("website") or "").strip()
        account_username = (form.get("account_username") or "").strip()
        password_plain = form.get("password") or ""
        notes = (form.get("notes") or "").strip()
        category_ids = form.getlist("category_ids")

        form_data = {
            "name": name,
            "website": website,
            "account_username": account_username,
            "notes": notes,
            "category_ids": [int(cid) for cid in category_ids if str(cid).isdigit()],
        }

        errors: list[str] = []
        if not name:
            errors.append("Name is required.")
        if not website:
            errors.append("Website is required.")
        if not account_username:
            errors.append("Username is required.")
        if not password_plain.strip():
            errors.append("Password is required.")

        if len(name) > 120:
            errors.append("Name must be 120 characters or fewer.")
        if len(website) > 200:
            errors.append("Website must be 200 characters or fewer.")
        if len(account_username) > 120:
            errors.append("Username must be 120 characters or fewer.")
        if len(notes) > 500:
            errors.append("Notes must be 500 characters or fewer.")

        if errors:
            return None, errors, form_data

        entry = PasswordEntry(
            name=name,
            website=website,
            account_username=account_username,
            password_value=password_plain,
            notes=notes or None,
            created_by_user_id=user_id,
            updated_by_user_id=user_id,
        )

        ids = [int(cid) for cid in category_ids if str(cid).isdigit()]
        entry.categories = Category.query.filter(Category.id.in_(ids)).all() if ids else []

        db.session.add(entry)
        db.session.commit()

        return entry, [], form_data

    def update_password_entry(self, entry: PasswordEntry, form, *, user_id: int):
        name = (form.get("name") or "").strip()
        website = (form.get("website") or "").strip()
        account_username = (form.get("account_username") or "").strip()
        password_plain = form.get("password") or ""
        notes = (form.get("notes") or "").strip()
        category_ids = form.getlist("category_ids")

        form_data = {
            "name": name,
            "website": website,
            "account_username": account_username,
            "notes": notes,
            "category_ids": [int(cid) for cid in category_ids if str(cid).isdigit()],
        }

        errors: list[str] = []
        if not name:
            errors.append("Name is required.")
        if not website:
            errors.append("Website is required.")
        if not account_username:
            errors.append("Username is required.")

        if len(name) > 120:
            errors.append("Name must be 120 characters or fewer.")
        if len(website) > 200:
            errors.append("Website must be 200 characters or fewer.")
        if len(account_username) > 120:
            errors.append("Username must be 120 characters or fewer.")
        if len(notes) > 500:
            errors.append("Notes must be 500 characters or fewer.")

        if errors:
            return errors, form_data

        entry.name = name
        entry.website = website
        entry.account_username = account_username
        entry.notes = notes or None
        entry.updated_by_user_id = user_id

        if password_plain.strip():
            entry.password_value = password_plain

        ids = [int(cid) for cid in category_ids if str(cid).isdigit()]
        entry.categories = Category.query.filter(Category.id.in_(ids)).all() if ids else []

        db.session.commit()

        return [], form_data

    def delete_password_entry(self, entry: PasswordEntry) -> None:
        db.session.delete(entry)
        db.session.commit()