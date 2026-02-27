from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user

from app.services.password_service import PasswordService

password_bp = Blueprint("password", __name__)
password_service = PasswordService()


@password_bp.route("/dashboard")
@login_required
def dashboard():
    return render_template(
        "dashboard.html",
        categories=password_service.list_categories(),
        active_tab="passwords",
    )


@password_bp.route("/passwords/new", methods=["GET", "POST"])
@login_required
def new_password():
    categories = password_service.list_categories()
    form_data = {}

    if request.method == "POST":
        _entry, errors, form_data = password_service.create_password_entry(
            request.form,
            user_id=current_user.id,
        )

        if errors:
            for e in errors:
                flash(e, "danger")
        else:
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
    categories = password_service.list_categories()
    entry = password_service.get_entry_or_404(entry_id)

    if request.method == "POST":
        errors, form_data = password_service.update_password_entry(
            entry,
            request.form,
            user_id=current_user.id,
        )

        if errors:
            for e in errors:
                flash(e, "danger")
        else:
            flash("Password updated successfully.", "success")
            return redirect(url_for("password.dashboard"))
    else:
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
    entry = password_service.get_entry_or_404(entry_id)
    password_service.delete_password_entry(entry)

    flash("Password deleted successfully.", "success")
    return redirect(url_for("password.dashboard"))