from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required

from app.services.category_service import CategoryService

category_bp = Blueprint("category", __name__)
category_service = CategoryService()


@category_bp.route("/categories")
@login_required
def categories():
    return render_template(
        "categories.html",
        categories=category_service.list_categories(),
        active_tab="categories",
    )


@category_bp.route("/categories/new", methods=["GET", "POST"])
@login_required
def new_category():
    form_data = {}

    if request.method == "POST":
        _cat, errors, form_data = category_service.create_category(request.form)

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
    cat = category_service.get_category(category_id)

    if request.method == "POST":
        errors, form_data = category_service.update_category(cat, request.form)

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
    cat = category_service.get_category(category_id)
    category_service.delete_category(cat)

    flash("Category deleted successfully.", "success")
    return redirect(url_for("category.categories"))