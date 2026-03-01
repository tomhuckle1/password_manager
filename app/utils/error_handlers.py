from flask import jsonify, request
from werkzeug.exceptions import HTTPException


def register_error_handlers(app) -> None:
    @app.errorhandler(HTTPException)
    def handle_http_exception(err: HTTPException):
        # log 4xx as info, 5xx as warning
        level = "warning" if err.code and err.code >= 500 else "info"
        getattr(app.logger, level)(
            "HTTP %s %s %s", err.code, request.method, request.path
        )
        return jsonify({"error": err.name}), err.code

    @app.errorhandler(Exception)
    def handle_unhandled_exception(err: Exception):
        app.logger.exception("Unhandled exception on %s %s", request.method, request.path)
        return jsonify({"error": "Internal server error"}), 500