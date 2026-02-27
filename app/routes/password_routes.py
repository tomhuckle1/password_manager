from flask import Blueprint, render_template
from flask_login import login_required

from app.models.category import Category

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