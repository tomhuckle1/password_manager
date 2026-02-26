from flask_login import login_user, logout_user

from app import bcrypt
from app.models.user import User, ROLE_ADMIN, ROLE_REGULAR
from app.repositories.user_repository import UserRepository


class AuthService:
    def __init__(self, users: UserRepository):
        self.users = users

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
        pw_hash = bcrypt.generate_password_hash(password).decode("utf-8")

        user = User(
            name=name,
            email=email,
            password_hash=pw_hash,
            role=role,
        )

        self.users.add(user)
        return user, []

    def login_with_credentials(self, form):
        email = (form.get("email") or "").strip().lower()
        password = form.get("password") or ""

        user = self.users.get_by_email(email)
        if not user or not bcrypt.check_password_hash(user.password_hash, password):
            return None, ["Invalid email or password."]

        login_user(user)
        return user, []

    def logout_current_user(self):
        logout_user()