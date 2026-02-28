from __future__ import annotations

from flask_login import current_user

from app.models.password import PasswordEntry
from app.repositories.password_repository import PasswordRepository
from app.repositories.category_repository import CategoryRepository
from app.utils.encryptor import Encryptor
from app.utils.validators import validate_password_entry_form


class PasswordService:
    def __init__(
        self,
        passwords: PasswordRepository,
        categories: CategoryRepository,
        encryptor: Encryptor,
    ):
        self.passwords = passwords
        self.categories = categories
        self.encryptor = encryptor

    def list_categories(self):
        return self.categories.list_ordered()

    def get_entry_or_404(self, entry_id: int) -> PasswordEntry:
        return self.passwords.get_or_404(entry_id)

    def get_decrypted_password_for_entry(self, entry: PasswordEntry) -> str:
        return self.encryptor.decrypt(entry.password_value)

    def create_password_entry(self, form):
        category_ids = form.getlist("category_ids")
        #Validate
        data, errors = validate_password_entry_form(
            name=form.get("name"),
            website=form.get("website"),
            account_username=form.get("account_username"),
            password_plain=form.get("password"),
            notes=form.get("notes"),
        )
        if errors:
            return None, errors

        entry = PasswordEntry(
            name=data["name"],
            website=data["website"],
            account_username=data["account_username"],
            password_value=self.encryptor.encrypt(data["password_plain"]),
            notes=data["notes"],
            created_by_user_id=current_user.id,
            updated_by_user_id=current_user.id,
        )
        self._apply_categories(entry, category_ids)
        # Create password
        self.passwords.add(entry)

        return entry, []

    def update_password_entry(self, entry: PasswordEntry, form):
        # Get list of categories
        category_ids = form.getlist("category_ids")

        # Validate
        data, errors = validate_password_entry_form(
            name=form.get("name"),
            website=form.get("website"),
            account_username=form.get("account_username"),
            password_plain=form.get("password"),
            notes=form.get("notes"),
            require_password=False,
        )
        if errors:
            return errors

        entry.name = data["name"]
        entry.website = data["website"]
        entry.account_username = data["account_username"]
        entry.notes = data["notes"]
        entry.updated_by_user_id = current_user.id

        # Only update if new password entered
        if data["password_plain"].strip():
            # Encrypt
            entry.password_value = self.encryptor.encrypt(data["password_plain"])

        self._apply_categories(entry, category_ids)
        self.passwords.commit()

        return []

    def delete_password_entry(self, entry: PasswordEntry) -> None:
        self.passwords.delete(entry)

    # Helper
    def _apply_categories(self, entry: PasswordEntry, category_ids) -> None:
        # Change cat id's from form into int
        ids = [int(cid) for cid in category_ids if str(cid).isdigit()]
        # Get categories from provided id's
        entry.categories = self.categories.get_by_ids(ids)