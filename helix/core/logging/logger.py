import logging
import os
from logging.handlers import RotatingFileHandler

MAX_FILE_SIZE = 10 * 1024 * 1024

COLORS = {
    'DEBUG': '\033[36m',
    'INFO': '\033[32m',
    'WARNING': '\033[33m',
    'ERROR': '\033[31m',
    'CRITICAL': '\033[1;41m',
}
RESET = '\033[0m'

class ColoredFormatter(logging.Formatter):
    def format(self, record):
        levelname = record.levelname
        if levelname in COLORS:
            record.levelname = f"{COLORS[levelname]}{levelname}{RESET}"
        formatted = super().format(record)
        record.levelname = levelname
        return formatted

def setup_logger(app):
    if getattr(app, "_logger_configured", False):
        return

    log_dir = os.path.join(os.getcwd(), "logs")
    os.makedirs(log_dir, exist_ok=True)

    file_handler = RotatingFileHandler(
        os.path.join(log_dir, "server.log"),
        maxBytes=MAX_FILE_SIZE,
        backupCount=10,
        encoding='utf-8'
    )
    file_formatter = logging.Formatter(
        '[%(asctime)s] %(levelname)s - %(module)s:%(lineno)d - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    file_handler.setFormatter(file_formatter)

    console_handler = logging.StreamHandler()
    console_formatter = ColoredFormatter(
        '[%(asctime)s] %(levelname)s - %(module)s:%(lineno)d - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    console_handler.setFormatter(console_formatter)

    app.logger.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.addHandler(console_handler)
    app.logger.propagate = False
    app._logger_configured = True

    app.logger.info("Logger configurado com sucesso")
