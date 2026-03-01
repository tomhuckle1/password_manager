import logging
import os
import sys


def configure_logging(app):
    level_name = os.getenv("LOG_LEVEL", "INFO").upper()
    log_level = getattr(logging, level_name, logging.INFO)

    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(log_level)

    formatter = logging.Formatter(
        "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
    )
    handler.setFormatter(formatter)

    app.logger.setLevel(log_level)
    app.logger.addHandler(handler)

    logging.getLogger("werkzeug").setLevel(logging.WARNING)