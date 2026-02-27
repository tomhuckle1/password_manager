from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from app.models.category import Category
from app.models.password import PasswordEntry

password_bp = Blueprint("password", __name__)


@password_bp.route("/dashboard")
@login_required
def dashboard():
    categories = Category.query.order_by(Category.name).all()
    return render_template(
        "dashboard.html",
        categories=categories,
        active_tab="passwords",
    )


@password_bp.route("/passwords/new", methods=["GET", "POST"])
@login_required
def new_password():
    categories = Category.query.order_by(Category.name).all()
    form_data = {}

    if request.method == "POST":
        name = (request.form.get("name") or "").strip()
        website = (request.form.get("website") or "").strip()
        account_username = (request.form.get("account_username") or "").strip()
        password_plain = request.form.get("password") or ""
        notes = (request.form.get("notes") or "").strip()
        category_ids = request.form.getlist("category_ids")

        form_data = {
            "name": name,
            "website": website,
            "account_username": account_username,
            "notes": notes,
            "category_ids": [int(cid) for cid in category_ids if str(cid).isdigit()],
        }

        errors: list[str] = []
        if not name:
            errors.append("Name is required.")
        if not website:
            errors.append("Website is required.")
        if not account_username:
            errors.append("Username is required.")
        if not password_plain.strip():
            errors.append("Password is required.")

        if len(name) > 120:
            errors.append("Name must be 120 characters or fewer.")
        if len(website) > 200:
            errors.append("Website must be 200 characters or fewer.")
        if len(account_username) > 120:
            errors.append("Username must be 120 characters or fewer.")
        if len(notes) > 500:
            errors.append("Notes must be 500 characters or fewer.")

        if errors:
            for e in errors:
                flash(e, "danger")
            return render_template(
                "password_form.html",
                categories=categories,
                active_tab="passwords",
                form_data=form_data,
                form_mode="create",
            )

        entry = PasswordEntry(
            name=name,
            website=website,
            account_username=account_username,
            password_value=password_plain,
            notes=notes or None,
            created_by_user_id=current_user.id,
            updated_by_user_id=current_user.id,
        )

        ids = [int(cid) for cid in category_ids if str(cid).isdigit()]
        entry.categories = Category.query.filter(Category.id.in_(ids)).all() if ids else []

        db.session.add(entry)
        db.session.commit()

        flash("Password created successfully.", "success")
        return redirect(url_for("password.dashboard"))

    return render_template(
        "password_form.html",
        categories=categories,
        active_tab="passwords",
        form_data=form_data,
        form_mode="create",
    )


@password_bp.route("/passwords/<int:entry_id>/edit", methods=["GET", "POST"])
@login_required
def edit_password(entry_id: int):
    categories = Category.query.order_by(Category.name).all()
    entry = PasswordEntry.query.get_or_404(entry_id)

    if request.method == "POST":
        name = (request.form.get("name") or "").strip()
        website = (request.form.get("website") or "").strip()
        account_username = (request.form.get("account_username") or "").strip()
        password_plain = request.form.get("password") or ""
        notes = (request.form.get("notes") or "").strip()
        category_ids = request.form.getlist("category_ids")

        form_data = {
            "name": name,
            "website": website,
            "account_username": account_username,
            "notes": notes,
            "category_ids": [int(cid) for cid in category_ids if str(cid).isdigit()],
        }

        errors: list[str] = []
        if not name:
            errors.append("Name is required.")
        if not website:
            errors.append("Website is required.")
        if not account_username:
            errors.append("Username is required.")

        if len(name) > 120:
            errors.append("Name must be 120 characters or fewer.")
        if len(website) > 200:
            errors.append("Website must be 200 characters or fewer.")
        if len(account_username) > 120:
            errors.append("Username must be 120 characters or fewer.")
        if len(notes) > 500:
            errors.append("Notes must be 500 characters or fewer.")

        if errors:
            for e in errors:
                flash(e, "danger")
            return render_template(
                "password_form.html",
                categories=categories,
                active_tab="passwords",
                form_data=form_data,
                form_mode="edit",
                entry_id=entry.id,
            )

        entry.name = name
        entry.website = website
        entry.account_username = account_username
        entry.notes = notes or None
        entry.updated_by_user_id = current_user.id

        # Only update password if user typed one
        if password_plain.strip():
            entry.password_value = password_plain

        ids = [int(cid) for cid in category_ids if str(cid).isdigit()]
        entry.categories = Category.query.filter(Category.id.in_(ids)).all() if ids else []

        db.session.commit()

        flash("Password updated successfully.", "success")
        return redirect(url_for("password.dashboard"))

    # GET
    form_data = {
        "name": entry.name or "",
        "website": entry.website or "",
        "account_username": entry.account_username or "",
        "notes": entry.notes or "",
        "category_ids": [c.id for c in (entry.categories or [])],
    }

    return render_template(
        "password_form.html",
        categories=categories,
        active_tab="passwords",
        form_data=form_data,
        form_mode="edit",
        entry_id=entry.id,
    )


@password_bp.route("/passwords/<int:entry_id>/delete", methods=["POST"])
@login_required
def delete_password(entry_id: int):
    entry = PasswordEntry.query.get_or_404(entry_id)

    db.session.delete(entry)
    db.session.commit()

    flash("Password deleted successfully.", "success")
    return redirect(url_for("password.dashboard"))