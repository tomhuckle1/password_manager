from flask import Blueprint, render_template, jsonify, request, flash, redirect, url_for, current_app
from flask_login import login_required, current_user

password_bp = Blueprint("password", __name__)


def password_service():
    return current_app.extensions["services"]["password"]


@password_bp.route("/dashboard")
@login_required
def dashboard():
    return render_template(
        "dashboard.html",
        categories=password_service().list_categories(),
        active_tab="passwords",
    )

@password_bp.route("/api/password/<int:entry_id>/password", methods=["POST"])
@login_required
def api_get_password(entry_id: int):
    entry = password_service().get_entry_or_404(entry_id)

    try:
        pw = password_service().get_decrypted_password_for_entry(entry)
        return jsonify({"password": pw})
    except Exception:
        return jsonify({"error": "Unable to decrypt password"}), 400


@password_bp.route("/passwords/new", methods=["GET", "POST"])
@login_required
def new_password():
    categories = password_service().list_categories()
    form_data = {}

    if request.method == "POST":
        _entry, errors = password_service().create_password_entry(request.form)

        if errors:
            for e in errors:
                flash(e, "danger")

            form_data = {
                "name": request.form.get("name", "").strip(),
                "website": request.form.get("website", "").strip(),
                "account_username": request.form.get("account_username", "").strip(),
                "notes": request.form.get("notes", "").strip(),
                "category_ids": [
                    int(cid) for cid in request.form.getlist("category_ids") if cid.isdigit()
                ],
            }
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
    categories = password_service().list_categories()
    entry = password_service().get_entry_or_404(entry_id)

    if request.method == "POST":
        errors = password_service().update_password_entry(entry, request.form)

        if errors:
            for e in errors:
                flash(e, "danger")

            form_data = {
                "name": request.form.get("name", "").strip(),
                "website": request.form.get("website", "").strip(),
                "account_username": request.form.get("account_username", "").strip(),
                "notes": request.form.get("notes", "").strip(),
                "category_ids": [
                    int(cid) for cid in request.form.getlist("category_ids") if cid.isdigit()
                ],
            }
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
        entry_id=entry.id,
        form_mode="edit",
    )


@password_bp.route("/passwords/<int:entry_id>/delete", methods=["POST"])
@login_required
def delete_password(entry_id: int):
    entry = password_service().get_entry_or_404(entry_id)
    password_service().delete_password_entry(entry)

    flash("Password deleted successfully.", "success")
    return redirect(url_for("password.dashboard"))