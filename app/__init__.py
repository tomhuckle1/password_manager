from pathlib import Path
from dotenv import load_dotenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()

login_manager.session_protection = "strong"

def create_app(config_overrides: dict | None = None) -> Flask:
    load_dotenv()

    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object("app.config.Config")

    if config_overrides:
        app.config.update(config_overrides)

    Path(app.instance_path).mkdir(parents=True, exist_ok=True)

    db.init_app(app)
    migrate.init_app(app, db)

    from app import models  

    @app.get("/")
    def health():
        return {"status": "ok"}

    return app