from flask_login import login_user, logout_user

from app import db
from app.models import User, Category, PasswordEntry
from app.repositories.sqlalchemy_category_repository import SqlAlchemyCategoryRepository
from app.repositories.sqlalchemy_password_repository import SqlAlchemyPasswordRepository
from app.services.password_service import PasswordService
from app.utils.encryptor import FernetEncryptor


TOM_NAME = "Tom Huckle"
TOM_EMAIL = "tom@google.com"


class DummyForm(dict):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._lists = {}

    def get(self, key, default=None):
        return super().get(key, default)

    def setlist(self, key, values):
        self._lists[key] = list(values)

    def getlist(self, key):
        return list(self._lists.get(key, []))


# Helpers

def request_ctx(app, path, method="POST"):
    return app.test_request_context(path, method=method)


def make_password_service(app) -> PasswordService:
    return PasswordService(
        passwords=SqlAlchemyPasswordRepository(db),
        categories=SqlAlchemyCategoryRepository(db),
        encryptor=FernetEncryptor(app.config["ENCRYPTION_KEY"]),
    )


def build_password_form(
    *,
    name="Google",
    website="google.com",
    account_username="Tom Huckle",
    password="MyGoogle1!",
    notes="test note",
    category_ids=(),
    **overrides,
) -> DummyForm:
    data = {
        "name": name,
        "website": website,
        "account_username": account_username,
        "password": password,
        "notes": notes,
    }
    data.update(overrides)

    form = DummyForm(**data)
    form.setlist("category_ids", [str(x) for x in category_ids])
    return form


def create_user_in_db(app, *, email=TOM_EMAIL, name=TOM_NAME, is_admin=False) -> int:
    with app.app_context():
        user = User(
            name=name,
            email=email,
            password_hash="password",
            role="admin" if is_admin else "regular",
        )
        db.session.add(user)
        db.session.commit()
        return user.id


def login_as(user_id: int):
    user = db.session.get(User, user_id)
    login_user(user)


def create_categories_in_db(app):
    with app.app_context():
        c1 = Category(name="Work", description="Google accounts")
        c2 = Category(name="Personal", description="Google accounts")
        db.session.add_all([c1, c2])
        db.session.commit()
        return c1.id, c2.id


def create_password_entry_in_db(
    app,
    *,
    user_id: int,
    name="Google",
    website="google.com",
    account_username="Tom Huckle",
    raw_password="MyGoogle1!",
    notes="note",
    category_ids=(),
) -> int:
    with app.app_context():
        encryptor = FernetEncryptor(app.config["ENCRYPTION_KEY"])
        entry = PasswordEntry(
            name=name,
            website=website,
            account_username=account_username,
            password_value=encryptor.encrypt(raw_password),
            notes=notes,
            created_by_user_id=user_id,
            updated_by_user_id=user_id,
        )
        if category_ids:
            entry.categories = Category.query.filter(Category.id.in_(list(category_ids))).all()

        db.session.add(entry)
        db.session.commit()
        return entry.id


# Password tests

def test_create_password_entry_success_with_categories(app):
    user_id = create_user_in_db(app)
    cat1_id, cat2_id = create_categories_in_db(app)

    with request_ctx(app, "/passwords/new", method="POST"):
        with app.app_context():
            login_as(user_id)
            service = make_password_service(app)

            entry, errors = service.create_password_entry(
                build_password_form(category_ids=[cat1_id, cat2_id])
            )

            assert errors == []
            assert entry is not None
            assert entry.name == "Google"
            assert entry.website == "google.com"
            assert entry.account_username == "Tom Huckle"

            assert service.get_decrypted_password_for_entry(entry) == "MyGoogle1!"

            assert entry.created_by_user_id == user_id
            assert entry.updated_by_user_id == user_id
            assert sorted([c.id for c in entry.categories]) == sorted([cat1_id, cat2_id])

            logout_user()


def test_create_password_entry_validation_errors(app):
    user_id = create_user_in_db(app)

    with request_ctx(app, "/passwords/new", method="POST"):
        with app.app_context():
            login_as(user_id)
            service = make_password_service(app)

            entry, errors = service.create_password_entry(
                build_password_form(
                    name="",
                    website="",
                    account_username="",
                    password="",
                    notes="",
                    category_ids=[],
                )
            )

            assert entry is None
            assert "Name is required." in errors
            assert "Website is required." in errors
            assert "Username is required." in errors
            assert "Password is required." in errors

            logout_user()


def test_update_password_entry_updates_fields_but_keeps_password_if_blank(app):
    user_id = create_user_in_db(app)
    cat1_id, cat2_id = create_categories_in_db(app)

    entry_id = create_password_entry_in_db(
        app,
        user_id=user_id,
        raw_password="MyGoogle1!",
        category_ids=[cat1_id],
    )

    with request_ctx(app, f"/passwords/{entry_id}/edit", method="POST"):
        with app.app_context():
            login_as(user_id)
            service = make_password_service(app)

            form = build_password_form(
                name="Google Updated",
                password="   ",  
                notes="updated notes",
                category_ids=[cat2_id],
            )

            entry = db.session.get(PasswordEntry, entry_id)
            old_encrypted = entry.password_value

            errors = service.update_password_entry(entry, form)

            assert errors == []
            db.session.refresh(entry)

            assert entry.name == "Google Updated"
            assert entry.notes == "updated notes"
            assert entry.updated_by_user_id == user_id
            assert entry.password_value == old_encrypted
            assert [c.id for c in entry.categories] == [cat2_id]

            logout_user()


def test_update_password_entry_overwrites_password_when_provided(app):
    user_id = create_user_in_db(app)
    entry_id = create_password_entry_in_db(app, user_id=user_id, raw_password="MyGoogle1!")

    with request_ctx(app, f"/passwords/{entry_id}/edit", method="POST"):
        with app.app_context():
            login_as(user_id)
            service = make_password_service(app)

            form = build_password_form(password="NewPass1!", category_ids=[])

            entry = db.session.get(PasswordEntry, entry_id)
            errors = service.update_password_entry(entry, form)

            assert errors == []
            db.session.refresh(entry)
            assert service.get_decrypted_password_for_entry(entry) == "NewPass1!"

            logout_user()


def test_update_password_entry_validation_errors(app):
    user_id = create_user_in_db(app)
    entry_id = create_password_entry_in_db(app, user_id=user_id, raw_password="MyGoogle1!")

    with request_ctx(app, f"/passwords/{entry_id}/edit", method="POST"):
        with app.app_context():
            login_as(user_id)
            service = make_password_service(app)

            form = build_password_form(
                name="",
                website="",
                account_username="",
                password="",
                notes="",
                category_ids=[],
            )

            entry = db.session.get(PasswordEntry, entry_id)
            errors = service.update_password_entry(entry, form)

            assert "Name is required." in errors
            assert "Website is required." in errors
            assert "Username is required." in errors

            logout_user()


def test_delete_password_entry_removes_from_db(app):
    user_id = create_user_in_db(app)
    entry_id = create_password_entry_in_db(app, user_id=user_id, raw_password="MyGoogle1!")

    with app.app_context():
        service = make_password_service(app)
        entry = db.session.get(PasswordEntry, entry_id)

        service.delete_password_entry(entry)

        assert db.session.get(PasswordEntry, entry_id) is None