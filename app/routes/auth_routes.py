from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user, login_user, logout_user

from app import db, bcrypt
from app.models.user import User, ROLE_ADMIN, ROLE_REGULAR

auth_bp = Blueprint("auth", __name__)


def redirect_dashboard():
    return redirect(url_for("password.dashboard"))


@auth_bp.route("/", methods=["GET"])
def index():
    return redirect_dashboard() if current_user.is_authenticated else redirect(url_for("auth.login"))


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect_dashboard()

    if request.method == "GET":
        return render_template("register.html")

    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip().lower()
    password = request.form.get("password", "")
    confirm = request.form.get("confirm", "")
    is_admin = request.form.get("is_admin") == "on"

    errors = []
    if not name or not email or not password or not confirm:
        errors.append("All fields are required.")
    if password != confirm:
        errors.append("Passwords do not match.")
    if User.query.filter_by(email=email).first():
        errors.append("An account with that email already exists.")

    if errors:
        for e in errors:
            flash(e, "danger")
        return render_template("register.html")

    role = ROLE_ADMIN if is_admin else ROLE_REGULAR
    pw_hash = bcrypt.generate_password_hash(password).decode("utf-8")

    user = User(name=name, email=email, password_hash=pw_hash, role=role)
    db.session.add(user)
    db.session.commit()

    flash("Account created. Please log in.", "success")
    return redirect(url_for("auth.login"))


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect_dashboard()

    if request.method == "GET":
        return render_template("login.html")

    email = request.form.get("email", "").strip().lower()
    password = request.form.get("password", "")

    user = User.query.filter_by(email=email).first()
    if not user or not bcrypt.check_password_hash(user.password_hash, password):
        flash("Invalid email or password.", "danger")
        return render_template("login.html")

    login_user(user)
    flash("Logged in successfully.", "success")
    return redirect_dashboard()


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logged out successfully.", "success")
    return redirect(url_for("auth.login"))