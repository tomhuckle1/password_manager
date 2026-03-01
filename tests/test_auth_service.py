from flask_login import current_user

from app import db, bcrypt
from app.models import User
from app.models.user import ROLE_ADMIN, ROLE_REGULAR
from app.repositories.sqlalchemy_user_repository import SqlAlchemyUserRepository
from app.services.auth_service import AuthService
from app.utils.password_hashing import BcryptPasswordHasher


TOM_NAME = "Tom Huckle"
TOM_EMAIL = "tom@google.com"
TOM_PASSWORD = "Secure1!"


class DummyForm(dict):
    def get(self, key, default=None):
        return super().get(key, default)


# Helpers

def build_register_form(**overrides) -> DummyForm:
    data = {
        "name": TOM_NAME,
        "email": TOM_EMAIL,
        "password": TOM_PASSWORD,
        "confirm": TOM_PASSWORD,
    }
    data.update(overrides)
    return DummyForm(**data)


def build_login_form(email=TOM_EMAIL, password=TOM_PASSWORD) -> DummyForm:
    return DummyForm(email=email, password=password)


def make_auth_service() -> AuthService:
    return AuthService(
        users=SqlAlchemyUserRepository(db),
        hasher=BcryptPasswordHasher(bcrypt),
    )


def register_default_user(app, **overrides) -> User:
    with app.app_context():
        service = make_auth_service()
        user, errors, _data = service.register_user(build_register_form(**overrides))
        assert errors == []
        assert user is not None
        return user


# Register

def test_register_user_success_regular(app):
    with app.app_context():
        service = make_auth_service()
        user, errors, _ = service.register_user(build_register_form())

        assert errors == []
        assert user is not None
        assert user.name == TOM_NAME
        assert user.email == TOM_EMAIL
        assert user.role == ROLE_REGULAR
        assert user.password_hash != TOM_PASSWORD

        saved = User.query.filter_by(email=TOM_EMAIL).first()
        assert saved is not None


def test_register_user_success_admin(app):
    with app.app_context():
        service = make_auth_service()
        user, errors, _ = service.register_user(
            build_register_form(email="tom.admin@google.com", is_admin="on")
        )

        assert errors == []
        assert user is not None
        assert user.role == ROLE_ADMIN


def test_register_user_validation_errors(app):
    with app.app_context():
        service = make_auth_service()
        user, errors, _ = service.register_user(
            DummyForm(name="", email="", password="", confirm="")
        )

        assert user is None
        assert errors == ["All fields are required."]


def test_register_user_duplicate_email(app):
    register_default_user(app)

    with app.app_context():
        service = make_auth_service()
        user2, errors2, _ = service.register_user(
            build_register_form(name="Tom Huckle 2")
        )

        assert user2 is None
        assert "An account with that email already exists." in errors2


# Login

def test_login_with_credentials_success_sets_authenticated(app):
    register_default_user(app)

    with app.test_request_context("/login", method="POST"):
        service = make_auth_service()
        logged_in_user, errors = service.login_with_credentials(build_login_form())

        assert errors == []
        assert logged_in_user is not None
        assert current_user.is_authenticated is True
        assert current_user.email == TOM_EMAIL

        service.logout_current_user()
        assert current_user.is_authenticated is False


def test_login_with_credentials_invalid_password(app):
    register_default_user(app)

    with app.test_request_context("/login", method="POST"):
        service = make_auth_service()
        logged_in_user, errors = service.login_with_credentials(
            build_login_form(password="WrongPass1!")
        )

        assert logged_in_user is None
        assert "Invalid email or password." in errors
        assert current_user.is_authenticated is False


def test_login_with_credentials_unknown_email(app):
    with app.test_request_context("/login", method="POST"):
        service = make_auth_service()
        logged_in_user, errors = service.login_with_credentials(
            build_login_form(email="unknown@google.com")
        )

        assert logged_in_user is None
        assert "Invalid email or password." in errors
        assert current_user.is_authenticated is False


def test_login_with_credentials_validation_errors(app):
    with app.test_request_context("/login", method="POST"):
        service = make_auth_service()
        logged_in_user, errors = service.login_with_credentials(
            DummyForm(email="", password="")
        )

        assert logged_in_user is None
        assert "Email and password are required." in errors
        assert current_user.is_authenticated is False


# Logout

def test_logout_current_user_logs_out(app):
    register_default_user(app)

    with app.test_request_context("/logout"):
        service = make_auth_service()
        logged_in_user, errors = service.login_with_credentials(build_login_form())
        assert errors == []
        assert current_user.is_authenticated is True

        service.logout_current_user()
        assert current_user.is_authenticated is False