import logging
from logging.handlers import RotatingFileHandler

from .constants import BASE_DIR, DT_LOG_FORMAT, LOG_FORMAT


def configure_logging():
    log_dir = BASE_DIR / "logs"
    log_dir.mkdir(exist_ok=True)
    log_file = log_dir / "parser.log"
    rotating_handler = RotatingFileHandler(log_file, maxBytes=10**6, backupCount=5)
    logging.basicConfig(
        datefmt=DT_LOG_FORMAT,
        format=LOG_FORMAT,
        level=logging.INFO,
        handlers=(rotating_handler, logging.StreamHandler()),
    )
