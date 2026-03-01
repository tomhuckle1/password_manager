from app.models import User

TOM_NAME = "Tom Huckle"
TOM_EMAIL = "tom@google.com"
TOM_PASSWORD = "Secure1!"

# Helpers

def post_form(client, path: str, data: dict, *, follow_redirects=False):
    return client.post(path, data=data, follow_redirects=follow_redirects)


def build_register_data(**overrides) -> dict:
    data = {
        "name": TOM_NAME,
        "email": TOM_EMAIL,
        "password": TOM_PASSWORD,
        "confirm": TOM_PASSWORD,
    }
    data.update(overrides)
    return data


def build_login_data(**overrides) -> dict:
    data = {
        "email": TOM_EMAIL,
        "password": TOM_PASSWORD,
    }
    data.update(overrides)
    return data


def register_tom(client, **overrides):
    return post_form(client, "/register", build_register_data(**overrides), follow_redirects=False)


def login_tom(client, **overrides):
    return post_form(client, "/login", build_login_data(**overrides), follow_redirects=False)


# Routes

def test_register_page_loads(client):
    res = client.get("/register")
    assert res.status_code == 200
    assert b"Register" in res.data


def test_login_page_loads(client):
    res = client.get("/login")
    assert res.status_code == 200
    assert b"Login" in res.data


def test_index_redirects_to_login_when_logged_out(client):
    res = client.get("/", follow_redirects=False)
    assert res.status_code == 302
    assert "/login" in res.headers.get("Location", "")


def test_register_creates_user_and_redirects_to_login(app, client):
    res = register_tom(client)

    assert res.status_code == 302
    assert "/login" in res.headers.get("Location", "")

    with app.app_context():
        user = User.query.filter_by(email=TOM_EMAIL).first()
        assert user is not None
        assert user.name == TOM_NAME


def test_register_duplicate_email_shows_error(client):
    register_tom(client)

    res = register_tom(client)

    assert res.status_code == 200
    assert b"already exists" in res.data.lower()


def test_register_validation_error_shows_message(client):
    res = post_form(
        client,
        "/register",
        build_register_data(confirm=""),
        follow_redirects=True,
    )

    assert res.status_code == 200
    assert b"All fields are required." in res.data


def test_login_success_redirects_to_dashboard(client):
    register_tom(client)

    res = login_tom(client)

    assert res.status_code == 302
    assert "/dashboard" in res.headers.get("Location", "")


def test_login_failure_rerenders_login_with_error(client):
    register_tom(client)

    res = login_tom(client, password="WrongPass1!")

    assert res.status_code == 200
    assert b"Invalid email or password." in res.data


def test_login_redirects_to_dashboard_when_already_logged_in(client):
    register_tom(client)
    login_tom(client)

    res = client.get("/login", follow_redirects=False)
    assert res.status_code == 302
    assert "/dashboard" in res.headers.get("Location", "")


def test_logout_requires_login(client):
    res = client.get("/logout", follow_redirects=False)

    assert res.status_code in (302, 401)
    if res.status_code == 302:
        assert "/login" in res.headers.get("Location", "")


def test_logout_logs_out_and_redirects_to_login(client):
    register_tom(client)
    login_tom(client)

    res = client.get("/logout", follow_redirects=False)

    assert res.status_code == 302
    assert "/login" in res.headers.get("Location", "")

    res2 = client.get("/", follow_redirects=False)
    assert res2.status_code == 302
    assert "/login" in res2.headers.get("Location", "")