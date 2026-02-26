from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import login_required, current_user

auth_bp = Blueprint("auth", __name__)


def auth_service():
    return current_app.extensions["services"]["auth"]


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

    _user, errors = auth_service().register_user(request.form)

    if errors:
        for e in errors:
            flash(e, "danger")
        return render_template("register.html")

    flash("Account created. Please log in.", "success")
    return redirect(url_for("auth.login"))


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect_dashboard()

    if request.method == "GET":
        return render_template("login.html")

    _user, errors = auth_service().login_with_credentials(request.form)

    if errors:
        for e in errors:
            flash(e, "danger")
        return render_template("login.html")

    flash("Logged in successfully.", "success")
    return redirect_dashboard()


@auth_bp.route("/logout")
@login_required
def logout():
    auth_service().logout_current_user()
    flash("Logged out successfully.", "success")
    return redirect(url_for("auth.login"))