from __future__ import annotations
import re


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