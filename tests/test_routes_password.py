from app import db
from app.models import User, Category, PasswordEntry
from app.utils.encryptor import FernetEncryptor

TOM_NAME = "Tom Huckle"
TOM_EMAIL = "tom@google.com"
TOM_PASSWORD = "Secure1!"


# Helpers

def register_tom(client, *, is_admin: bool = False):
    data = {
        "name": TOM_NAME,
        "email": TOM_EMAIL,
        "password": TOM_PASSWORD,
        "confirm": TOM_PASSWORD,
    }
    if is_admin:
        data["is_admin"] = "on"
    return client.post("/register", data=data, follow_redirects=False)


def login_tom(client, *, password: str = TOM_PASSWORD):
    return client.post(
        "/login",
        data={"email": TOM_EMAIL, "password": password},
        follow_redirects=False,
    )


def create_category(app, *, name: str = "Work", description: str = "Google accounts") -> int:
    with app.app_context():
        cat = Category(name=name, description=description)
        db.session.add(cat)
        db.session.commit()
        return cat.id


def create_password_entry(app, *, user_email: str = TOM_EMAIL, category_ids=None) -> int:
    if category_ids is None:
        category_ids = []

    with app.app_context():
        user = User.query.filter_by(email=user_email).first()
        assert user is not None, "User must exist before creating password entry."

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

        if category_ids:
            entry.categories = Category.query.filter(Category.id.in_(category_ids)).all()

        db.session.add(entry)
        db.session.commit()
        return entry.id


# Routes

def test_dashboard_requires_login(client):
    res = client.get("/dashboard", follow_redirects=False)
    assert res.status_code in (302, 401)


def test_new_password_post_creates_entry_and_redirects(app, client):
    register_tom(client)
    login_tom(client)

    cat_id = create_category(app)

    res = client.post(
        "/passwords/new",
        data={
            "name": "Google",
            "website": "google.com",
            "account_username": TOM_NAME,
            "password": "MyGoogle1!",
            "notes": "note",
            "category_ids": [str(cat_id)],
        },
        follow_redirects=False,
    )

    assert res.status_code == 302
    assert "/dashboard" in res.headers.get("Location", "")

    with app.app_context():
        entry = PasswordEntry.query.filter_by(
            website="google.com", account_username=TOM_NAME
        ).first()
        assert entry is not None

        encryptor = FernetEncryptor(app.config["ENCRYPTION_KEY"])
        assert encryptor.decrypt(entry.password_value) == "MyGoogle1!"


def test_edit_password_post_updates_entry_and_redirects(app, client):
    register_tom(client)
    login_tom(client)

    entry_id = create_password_entry(app)

    res = client.post(
        f"/passwords/{entry_id}/edit",
        data={
            "name": "Google Updated",
            "website": "google.com",
            "account_username": TOM_NAME,
            "password": "",  
            "notes": "updated notes",
            "category_ids": [],
        },
        follow_redirects=False,
    )

    assert res.status_code == 302
    assert "/dashboard" in res.headers.get("Location", "")

    with app.app_context():
        entry = db.session.get(PasswordEntry, entry_id)
        assert entry is not None
        assert entry.name == "Google Updated"
        assert entry.notes == "updated notes"


def test_api_get_password_returns_decrypted_password_for_logged_in_user(app, client):
    register_tom(client, is_admin=False)
    login_tom(client)

    entry_id = create_password_entry(app)

    res = client.post(f"/api/password/{entry_id}/password", follow_redirects=False)
    assert res.status_code == 200

    data = res.get_json()
    assert data["password"] == "MyGoogle1!"


def test_delete_password_denied_for_non_admin(app, client):
    register_tom(client, is_admin=False)
    login_tom(client)

    entry_id = create_password_entry(app)

    res = client.post(f"/passwords/{entry_id}/delete", follow_redirects=False)
    assert res.status_code == 302
    assert "/dashboard" in res.headers.get("Location", "")

    with app.app_context():
        assert db.session.get(PasswordEntry, entry_id) is not None


def test_delete_password_succeeds_for_admin(app, client):
    register_tom(client, is_admin=True)
    login_tom(client)

    entry_id = create_password_entry(app)

    res = client.post(f"/passwords/{entry_id}/delete", follow_redirects=False)
    assert res.status_code == 302
    assert "/dashboard" in res.headers.get("Location", "")

    with app.app_context():
        assert db.session.get(PasswordEntry, entry_id) is None