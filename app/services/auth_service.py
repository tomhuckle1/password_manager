from flask_login import login_user, logout_user

from app.models.user import User, ROLE_ADMIN, ROLE_REGULAR
from app.repositories.user_repository import UserRepository
from app.utils.password_hashing import PasswordHasher


class AuthService:
    def __init__(self, users: UserRepository, hasher: PasswordHasher):
        self.users = users
        self.hasher = hasher

    def register_user(self, form):
        name = (form.get("name") or "").strip()
        email = (form.get("email") or "").strip().lower()
        password = form.get("password") or ""
        confirm = form.get("confirm") or ""
        is_admin = form.get("is_admin") == "on"

        errors: list[str] = []

        if not name or not email or not password or not confirm:
            errors.append("All fields are required.")
        if password != confirm:
            errors.append("Passwords do not match.")
        if self.users.get_by_email(email):
            errors.append("An account with that email already exists.")

        if errors:
            return None, errors

        role = ROLE_ADMIN if is_admin else ROLE_REGULAR

        user = User(
            name=name,
            email=email,
            password_hash=self.hasher.hash(password),
            role=role,
        )

        self.users.add(user)
        return user, []

    def login_with_credentials(self, form):
        email = (form.get("email") or "").strip().lower()
        password = form.get("password") or ""

        user = self.users.get_by_email(email)
        if not user or not self.hasher.verify(user.password_hash, password):
            return None, ["Invalid email or password."]

        login_user(user)
        return user, []

    def logout_current_user(self):
        logout_user()