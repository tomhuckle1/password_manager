from __future__ import annotations

from flask_login import current_user

from app.models.password import PasswordEntry
from app.repositories.password_repository import PasswordRepository
from app.repositories.category_repository import CategoryRepository


class PasswordService:
    def __init__(self, passwords: PasswordRepository, categories: CategoryRepository):
        self.passwords = passwords
        self.categories = categories

    def list_categories(self):
        return self.categories.list_ordered()

    def get_entry_or_404(self, entry_id: int) -> PasswordEntry:
        return self.passwords.get_or_404(entry_id)

    def create_password_entry(self, form):
        name = (form.get("name") or "").strip()
        website = (form.get("website") or "").strip()
        account_username = (form.get("account_username") or "").strip()
        password_plain = form.get("password") or ""
        notes = (form.get("notes") or "").strip()
        category_ids = form.getlist("category_ids")

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
            return None, errors

        entry = PasswordEntry(
            name=name,
            website=website,
            account_username=account_username,
            password_value=password_plain,
            notes=notes or None,
            created_by_user_id=current_user.id,
            updated_by_user_id=current_user.id,
        )

        self._apply_categories(entry, category_ids)
        self.passwords.add(entry)

        return entry, []

    def update_password_entry(self, entry: PasswordEntry, form):
        name = (form.get("name") or "").strip()
        website = (form.get("website") or "").strip()
        account_username = (form.get("account_username") or "").strip()
        password_plain = form.get("password") or ""
        notes = (form.get("notes") or "").strip()
        category_ids = form.getlist("category_ids")

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
            return errors

        entry.name = name
        entry.website = website
        entry.account_username = account_username
        entry.notes = notes or None
        entry.updated_by_user_id = current_user.id

        if password_plain.strip():
            entry.password_value = password_plain

        self._apply_categories(entry, category_ids)
        self.passwords.commit()

        return []

    def delete_password_entry(self, entry: PasswordEntry) -> None:
        self.passwords.delete(entry)

    def _apply_categories(self, entry: PasswordEntry, category_ids) -> None:
        ids = [int(cid) for cid in category_ids if str(cid).isdigit()]
        entry.categories = self.categories.get_by_ids(ids)