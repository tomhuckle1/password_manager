from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from app import db
from app.models.category import Category

category_bp = Blueprint("category", __name__)


@category_bp.route("/categories")
@login_required
def categories():
    categories = Category.query.order_by(Category.name).all()
    return render_template(
        "categories.html",
        categories=categories,
        active_tab="categories",
    )


@category_bp.route("/categories/new", methods=["GET", "POST"])
@login_required
def new_category():
    form_data = {}

    if request.method == "POST":
        name = (request.form.get("name") or "").strip()
        description = (request.form.get("description") or "").strip()

        form_data = {"name": name, "description": description}

        errors: list[str] = []
        if not name:
            errors.append("Name is required.")
        if len(name) > 60:
            errors.append("Name must be 60 characters or fewer.")
        if len(description) > 200:
            errors.append("Description must be 200 characters or fewer.")

        if errors:
            for e in errors:
                flash(e, "danger")
        else:
            cat = Category(name=name, description=description or None)
            db.session.add(cat)
            try:
                db.session.commit()
                flash("Category created successfully.", "success")
                return redirect(url_for("category.categories"))
            except Exception:
                db.session.rollback()
                flash("A category with that name already exists.", "danger")

    return render_template(
        "category_form.html",
        active_tab="categories",
        form_data=form_data,
        form_mode="create",
    )


@category_bp.route("/categories/<int:category_id>/edit", methods=["GET", "POST"])
@login_required
def edit_category(category_id: int):
    cat = Category.query.get_or_404(category_id)

    if request.method == "POST":
        name = (request.form.get("name") or "").strip()
        description = (request.form.get("description") or "").strip()

        form_data = {"name": name, "description": description}

        errors: list[str] = []
        if not name:
            errors.append("Name is required.")
        if len(name) > 60:
            errors.append("Name must be 60 characters or fewer.")
        if len(description) > 200:
            errors.append("Description must be 200 characters or fewer.")

        if errors:
            for e in errors:
                flash(e, "danger")
            return render_template(
                "category_form.html",
                active_tab="categories",
                form_data=form_data,
                form_mode="edit",
                category_id=cat.id,
            )

        cat.name = name
        cat.description = description or None

        try:
            db.session.commit()
            flash("Category updated successfully.", "success")
            return redirect(url_for("category.categories"))
        except Exception:
            db.session.rollback()
            flash("A category with that name already exists.", "danger")
            return render_template(
                "category_form.html",
                active_tab="categories",
                form_data=form_data,
                form_mode="edit",
                category_id=cat.id,
            )

    # GET
    form_data = {
        "name": cat.name or "",
        "description": cat.description or "",
    }
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
    cat = Category.query.get_or_404(category_id)

    db.session.delete(cat)
    try:
        db.session.commit()
        flash("Category deleted successfully.", "success")
    except Exception:
        db.session.rollback()
        flash("Could not delete category.", "danger")

    return redirect(url_for("category.categories"))