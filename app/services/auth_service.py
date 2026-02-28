from __future__ import annotations

from flask_login import login_user, logout_user

from app.models.user import User, ROLE_ADMIN, ROLE_REGULAR
from app.repositories.user_repository import UserRepository
from app.utils.password_hashing import PasswordHasher
from app.utils.validators import validate_register_form, validate_login_form


class AuthService:
    def __init__(self, users: UserRepository, hasher: PasswordHasher):
        self.users = users
        self.hasher = hasher

    def register_user(self, form):
        # Validate
        data, errors = validate_register_form(
            name=form.get("name"),
            email=form.get("email"),
            password=form.get("password"),
            confirm=form.get("confirm"),
        )

        if errors:
            return None, errors, data

        # Determine role
        is_admin = form.get("is_admin") == "on"
        role = ROLE_ADMIN if is_admin else ROLE_REGULAR

        # Check email does not already exist
        if self.users.get_by_email(data["email"]):
            return None, ["An account with that email already exists."], data

        # Create    
        user = User(
            name=data["name"],
            email=data["email"],
            password_hash=self.hasher.hash(data["password"]),
            role=role,
        )

        # Save to db
        self.users.add(user)
        return user, [], data

    def login_with_credentials(self, form):
        # Validate
        data, errors = validate_login_form(
            email=form.get("email"),
            password=form.get("password"),
        )

        if errors:
            return None, errors
        #Find user y email
        user = self.users.get_by_email(data["email"])

        #  Check password is correct
        if not user or not self.hasher.verify(user.password_hash, data["password"]):
            return None, ["Invalid email or password."]

        login_user(user)
        return user, []

    def logout_current_user(self):
        logout_user()