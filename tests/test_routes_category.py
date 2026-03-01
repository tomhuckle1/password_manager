from app import db
from app.models import User, Category, PasswordEntry
from app.utils.encryptor import FernetEncryptor

TOM_NAME = "Tom Huckle"
TOM_EMAIL = "tom@google.com"
TOM_PASSWORD = "Secure1!"


# Helpers

def post_form(client, path: str, data: dict, *, follow_redirects=False):
    return client.post(path, data=data, follow_redirects=follow_redirects)


def build_register_data(*, is_admin=False, **overrides) -> dict:
    data = {
        "name": TOM_NAME,
        "email": TOM_EMAIL,
        "password": TOM_PASSWORD,
        "confirm": TOM_PASSWORD,
    }
    if is_admin:
        data["is_admin"] = "on"
    data.update(overrides)
    return data


def build_login_data(**overrides) -> dict:
    data = {"email": TOM_EMAIL, "password": TOM_PASSWORD}
    data.update(overrides)
    return data


def build_category_data(**overrides) -> dict:
    data = {"name": "Work", "description": "Google accounts"}
    data.update(overrides)
    return data


def register_tom(client, *, is_admin: bool = False):
    return post_form(
        client,
        "/register",
        build_register_data(is_admin=is_admin),
        follow_redirects=False,
    )


def login_tom(client, *, password: str = TOM_PASSWORD):
    return post_form(
        client,
        "/login",
        build_login_data(password=password),
        follow_redirects=False,
    )


def create_category_in_db(app, *, name: str = "Work", description: str = "Google accounts") -> int:
    with app.app_context():
        cat = Category(name=name, description=description)
        db.session.add(cat)
        db.session.commit()
        return cat.id


def attach_password_to_category(app, *, category_id: int) -> int:
    with app.app_context():
        user = User.query.filter_by(email=TOM_EMAIL).first()
        assert user is not None, "User must exist before creating password entry."

        cat = db.session.get(Category, category_id)
        assert cat is not None

        encryptor = FernetEncryptor(app.config["ENCRYPTION_KEY"])

        entry = PasswordEntry(
            name="Google",
            website="google.com",
            account_username=TOM_NAME,
            password_value=encryptor.encrypt("MyGoogle1!"),
            notes="test note",
            created_by_user_id=user.id,
            updated_by_user_id=user.id,
        )
        entry.categories = [cat]

        db.session.add(entry)
        db.session.commit()
        return entry.id


# Routes

def test_categories_requires_login(client):
    res = client.get("/categories", follow_redirects=False)
    assert res.status_code in (302, 401)


def test_create_category_post_creates_and_redirects(app, client):
    register_tom(client)
    login_tom(client)

    res = post_form(client, "/categories/new", build_category_data(), follow_redirects=False)

    assert res.status_code == 302
    assert "/categories" in res.headers.get("Location", "")

    with app.app_context():
        cat = Category.query.filter_by(name="Work").first()
        assert cat is not None
        assert cat.description == "Google accounts"


def test_edit_category_post_updates_and_redirects(app, client):
    register_tom(client)
    login_tom(client)

    cat_id = create_category_in_db(app, name="Work", description="Google accounts")

    res = post_form(
        client,
        f"/categories/{cat_id}/edit",
        build_category_data(name="Work Updated", description="Google accounts updated"),
        follow_redirects=False,
    )

    assert res.status_code == 302
    assert "/categories" in res.headers.get("Location", "")

    with app.app_context():
        cat = db.session.get(Category, cat_id)
        assert cat is not None
        assert cat.name == "Work Updated"
        assert cat.description == "Google accounts updated"


def test_delete_category_denied_for_non_admin(app, client):
    register_tom(client, is_admin=False)
    login_tom(client)

    cat_id = create_category_in_db(app)

    res = post_form(client, f"/categories/{cat_id}/delete", data={}, follow_redirects=False)

    assert res.status_code == 302

    with app.app_context():
        assert db.session.get(Category, cat_id) is not None


def test_delete_category_blocked_when_contains_passwords_even_for_admin(app, client):
    register_tom(client, is_admin=True)
    login_tom(client)

    cat_id = create_category_in_db(app)
    attach_password_to_category(app, category_id=cat_id)

    res = post_form(client, f"/categories/{cat_id}/delete", data={}, follow_redirects=False)

    assert res.status_code == 302

    with app.app_context():
        assert db.session.get(Category, cat_id) is not None


def test_delete_category_succeeds_for_admin_when_empty(app, client):
    register_tom(client, is_admin=True)
    login_tom(client)

    cat_id = create_category_in_db(app)

    res = post_form(client, f"/categories/{cat_id}/delete", data={}, follow_redirects=False)

    assert res.status_code == 302

    with app.app_context():
        assert db.session.get(Category, cat_id) is None