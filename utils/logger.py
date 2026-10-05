"""
logger.py — Structured dual-output logging.

Writes to console (INFO+) and file (DEBUG+) simultaneously.
Every log line is traceable: timestamp, level, module, function, message.
"""

import logging
import sys
from pathlib import Path

from config.settings import EXECUTION_LOG

_LOG_FORMAT = "%(asctime)s [ %(levelname)-5s ] [%(name)s.%(funcName)s] %(message)s"
_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

_configured_loggers = set()


class _StepFormatter(logging.Formatter):
    """Custom formatter that right-pads log level to 5 chars."""
    def format(self, record):
        if record.levelname == "WARNING":
            record.levelname = "WARN"
        return super().format(record)


def _ensure_log_dir():
    """Ensures the parent directory for EXECUTION_LOG exists."""
    Path(EXECUTION_LOG).parent.mkdir(parents=True, exist_ok=True)


def get_logger(name: str) -> logging.Logger:
    """
    Returns a configured logger instance.
    Logger name should typically be __name__ of the calling module.

    Configuration is applied once per logger name — safe to call repeatedly.
    """
    logger = logging.getLogger(name)

    if name in _configured_loggers:
        return logger

    logger.setLevel(logging.DEBUG)
    logger.propagate = False

    formatter = _StepFormatter(_LOG_FORMAT, datefmt=_DATE_FORMAT)

    # Console handler — INFO and above
    console = logging.StreamHandler(sys.stdout)
    console.setLevel(logging.INFO)
    console.setFormatter(formatter)
    logger.addHandler(console)

    # File handler — DEBUG and above
    _ensure_log_dir()
    file_handler = logging.FileHandler(EXECUTION_LOG, mode="a", encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    _configured_loggers.add(name)
    return logger
