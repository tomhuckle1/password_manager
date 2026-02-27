from __future__ import annotations
import re

# Auth 
def validate_register_form(
    *,
    name: str | None,
    email: str | None,
    password: str | None,
    confirm: str | None,
) -> tuple[dict, list[str]]:

    errors: list[str] = []

    name_clean = (name or "").strip()
    email_clean = (email or "").strip().lower()
    pw = password or ""
    conf = confirm or ""

    if not name_clean or not email_clean or not pw or not conf:
        errors.append("All fields are required.")
        return {
            "name": name_clean,
            "email": email_clean,
            "password": pw,
            "confirm": conf,
        }, errors

    if pw != conf:
        errors.append("Passwords do not match.")

    # Password rules
    if len(pw) < 8:
        errors.append("Password must be at least 8 characters.")

    if not re.search(r"[A-Z]", pw):
        errors.append("Password must contain at least one uppercase letter.")

    if not re.search(r"[a-z]", pw):
        errors.append("Password must contain at least one lowercase letter.")

    if not re.search(r"\d", pw):
        errors.append("Password must contain at least one number.")

    if not re.search(r"[^\w\s]", pw):
        errors.append("Password must contain at least one symbol.")

    data = {
        "name": name_clean,
        "email": email_clean,
        "password": pw,
        "confirm": conf,
    }

    return data, errors


def validate_login_form(
    *,
    email: str | None,
    password: str | None,
) -> tuple[dict, list[str]]:

    errors: list[str] = []

    email_clean = (email or "").strip().lower()
    pw = password or ""

    if not email_clean or not pw:
        errors.append("Email and password are required.")

    return {
        "email": email_clean,
        "password": pw,
    }, errors

# Category
def validate_category_form(*, name: str | None, description: str | None):
    errors: list[str] = []

    name_clean = (name or "").strip()
    description_clean = (description or "").strip()

    if not name_clean:
        errors.append("Name is required.")
    if len(name_clean) > 60:
        errors.append("Name must be 60 characters or fewer.")
    if len(description_clean) > 200:
        errors.append("Description must be 200 characters or fewer.")

    data = {
        "name": name_clean,
        "description": description_clean or None,
    }

    return data, errors

URL_REGEX = re.compile(r"^(?:[a-z0-9-]+\.)+[a-z]{2,63}(?:/.*)?$", re.IGNORECASE)


# Passwords
def clean_website(website: str | None) -> str:
    if not website:
        return ""

    s = website.strip().lower()
    s = s.removeprefix("https://").removeprefix("http://").removeprefix("www.")
    return s[:-1] if s.endswith("/") else s


def validate_password_entry_form(
    *,
    name: str | None,
    website: str | None,
    account_username: str | None,
    password_plain: str | None,
    notes: str | None = None,
    require_password: bool = True,
) -> tuple[dict, list[str]]:
    errors: list[str] = []

    name_clean = (name or "").strip()
    website_clean = clean_website(website)
    username_clean = (account_username or "").strip()
    pw = password_plain or ""
    notes_clean = (notes or "").strip()

    if not name_clean:
        errors.append("Name is required.")
    if not website_clean:
        errors.append("Website is required.")
    if not username_clean:
        errors.append("Username is required.")
    if require_password and not pw.strip():
        errors.append("Password is required.")

    if len(name_clean) > 120:
        errors.append("Name must be 120 characters or fewer.")
    if len(website_clean) > 200:
        errors.append("Website must be 200 characters or fewer.")
    if len(username_clean) > 120:
        errors.append("Username must be 120 characters or fewer.")
    if len(notes_clean) > 500:
        errors.append("Notes must be 500 characters or fewer.")

    if website_clean and not URL_REGEX.match(website_clean):
        errors.append("Website must be a valid domain (e.g. example.com).")

    data = {
        "name": name_clean,
        "website": website_clean,
        "account_username": username_clean,
        "password_plain": pw,
        "notes": notes_clean or None,
    }

    return data, errors