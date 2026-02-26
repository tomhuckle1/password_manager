from flask import Flask


def create_app(config_overrides: dict | None = None) -> Flask:
    app = Flask(__name__)

    app.config.from_object("app.config.Config")

    if config_overrides:
        app.config.update(config_overrides)

    @app.get("/")
    def health():
        return {"status": "ok"}

    return app