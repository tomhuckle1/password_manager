from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import login_required, current_user

# Blueprint
category_bp = Blueprint("category", __name__)


def category_service():
    return current_app.extensions["services"]["category"]


@category_bp.route("/categories")
@login_required
def categories():
    # Show categories
    return render_template(
        "categories.html",
        categories=category_service().list_categories(),
        active_tab="categories",
    )


@category_bp.route("/categories/new", methods=["GET", "POST"])
@login_required
def new_category():
    form_data = {}

    # Create category
    if request.method == "POST":
        _cat, errors, form_data = category_service().create_category(request.form)

        if errors:
            for e in errors:
                flash(e, "danger")
        else:
            flash("Category created successfully.", "success")
            return redirect(url_for("category.categories"))

    return render_template(
        "category_form.html",
        active_tab="categories",
        form_data=form_data,
        form_mode="create",
    )


@category_bp.route("/categories/<int:category_id>/edit", methods=["GET", "POST"])
@login_required
def edit_category(category_id: int):
    cat = category_service().get_category(category_id)

    # Edit category
    if request.method == "POST":
        errors, form_data = category_service().update_category(cat, request.form)

        if errors:
            for e in errors:
                flash(e, "danger")
        else:
            flash("Category updated successfully.", "success")
            return redirect(url_for("category.categories"))
    else:
        form_data = {"name": cat.name or "", "description": cat.description or ""}

    return render_template(
        "category_form.html",
        active_tab="categories",
        form_data=form_data,
        form_mode="edit",
        category_id=cat.id,
    )


@category_bp.route("/categories/<int:category_id>/delete", methods=["POST"])
@login_required
def delete_category(category_id: int):
    # Ensure user is admin
    if not current_user.is_admin():
        flash("You do not have permission to delete categories.", "danger")
        return redirect(url_for("category.categories"))

    cat = category_service().get_category(category_id)

    # Check passwords are not assigned to category
    if not category_service().can_delete_category(cat):
        flash(
            "Cannot delete category while it contains passwords. "
            "Delete all passwords in this category first.",
            "danger",
        )
        return redirect(url_for("category.categories"))

    # Delete category
    category_service().delete_category(cat)
    flash("Category deleted successfully.", "success")
    return redirect(url_for("category.categories"))