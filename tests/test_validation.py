from app.utils.validators import (
    clean_website,
    validate_password_entry_form,
    validate_category_form,
    validate_register_form,
    validate_login_form,
)

def test_clean_website_empty_returns_empty_string():
    assert clean_website(None) == ""
    assert clean_website("") == ""
    assert clean_website("   ") == ""


def test_clean_website_normalizes_common_inputs():
    assert clean_website("HTTPS://WWW.GOOGLE.COM/") == "google.com"
    assert clean_website("www.google.com/search") == "google.com/search"
    assert clean_website("  google.com  ") == "google.com"


def test_validate_password_entry_form_success_trims_and_normalizes():
    data, errors = validate_password_entry_form(
        name=" Google Account ",
        website="https://www.google.com/",
        account_username=" Tom Huckle ",
        password_plain="Secure1!",
        notes=" personal account ",
    )

    assert errors == []
    assert data["name"] == "Google Account"
    assert data["website"] == "google.com"
    assert data["account_username"] == "Tom Huckle"
    assert data["password_plain"] == "Secure1!"
    assert data["notes"] == "personal account"


def test_validate_password_entry_form_missing_required_fields_returns_errors():
    data, errors = validate_password_entry_form(
        name="",
        website="",
        account_username="",
        password_plain="",
        notes=None,
    )

    assert "Name is required." in errors
    assert "Website is required." in errors
    assert "Username is required." in errors
    assert "Password is required." in errors


def test_validate_password_entry_form_password_optional_when_flag_false():
    data, errors = validate_password_entry_form(
        name="Google",
        website="google.com",
        account_username="Tom Huckle",
        password_plain="   ",
        notes="",
        require_password=False,
    )

    assert errors == []


def test_validate_category_form_success_trims_fields():
    data, errors = validate_category_form(
        name=" Work ",
        description=" Google accounts ",
    )

    assert errors == []
    assert data["name"] == "Work"
    assert data["description"] == "Google accounts"


def test_validate_category_form_name_required():
    data, errors = validate_category_form(
        name="   ",
        description="Google",
    )

    assert "Name is required." in errors


def test_validate_register_form_success_normalizes_name_and_email():
    data, errors = validate_register_form(
        name=" Tom Huckle ",
        email=" TOM@GOOGLE.COM ",
        password="Secure1!",
        confirm="Secure1!",
    )

    assert errors == []
    assert data["name"] == "Tom Huckle"
    assert data["email"] == "tom@google.com"


def test_validate_register_form_all_fields_required():
    data, errors = validate_register_form(
        name="",
        email="",
        password="",
        confirm="",
    )

    assert errors == ["All fields are required."]


def test_validate_register_form_password_mismatch_returns_error():
    data, errors = validate_register_form(
        name="Tom Huckle",
        email="tom@google.com",
        password="Secure1!",
        confirm="Secure1?",
    )

    assert "Passwords do not match." in errors


def test_validate_login_form_success_normalizes_email():
    data, errors = validate_login_form(
        email=" TOM@GOOGLE.COM ",
        password="Secure1!",
    )

    assert errors == []
    assert data["email"] == "tom@google.com"
    assert data["password"] == "Secure1!"


def test_validate_login_form_requires_both_fields():
    data, errors = validate_login_form(email="", password="")
    assert "Email and password are required." in errors