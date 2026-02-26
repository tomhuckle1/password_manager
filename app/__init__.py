from pathlib import Path
from dotenv import load_dotenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
bcrypt = Bcrypt()

login_manager.session_protection = "strong"
login_manager.login_view = "auth.login"


def create_app(config_overrides: dict | None = None) -> Flask:
    load_dotenv()

    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object("app.config.Config")

    if config_overrides:
        app.config.update(config_overrides)

    Path(app.instance_path).mkdir(parents=True, exist_ok=True)

    # Extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    bcrypt.init_app(app)

    # Blueprints
    from app.routes.auth_routes import auth_bp
    from app.routes.category_routes import category_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(category_bp)

    from app import models 

    from app.repositories.sqlalchemy_user_repository import SqlAlchemyUserRepository
    from app.services.auth_service import AuthService
    from app.repositories.sqlalchemy_category_repository import SqlAlchemyCategoryRepository
    from app.services.category_service import CategoryService
    from app.utils.password_hashing import BcryptPasswordHasher

    app.extensions.setdefault("services", {})

    app.extensions["services"]["auth"] = AuthService(
        users=SqlAlchemyUserRepository(db),
        hasher=BcryptPasswordHasher(bcrypt),
    )

    app.extensions["services"]["category"] = CategoryService(
        categories=SqlAlchemyCategoryRepository(db),
    )

    return app