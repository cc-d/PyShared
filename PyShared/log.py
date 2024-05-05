import os
from typing import Optional as Opt
from logging import getLogger, StreamHandler, Formatter
from logging.handlers import RotatingFileHandler

# Default constants from environment or hardcoded defaults
_LOG_NAME = os.getenv('PYSHARED_LOG_NAME', 'pyshared')
_LOG_FILE = os.getenv('PYSHARED_LOG_FILE', '/tmp/pyshared.log')
_LOG_LEVEL = os.getenv('PYSHARED_LOG_LEVEL', 'DEBUG').upper()
_LOG_FORMAT = os.getenv(
    'PYSHARED_LOG_FORMAT',
    '%(asctime)s - %(levelname)s - %(name)s - %(message)s',
)
_DATE_FORMAT = os.getenv('PYSHARED_DATE_FORMAT', '%Y-%m-%d %H:%M:%S')
_MAX_LOG_SIZE = int(
    os.getenv('PYSHARED_MAX_LOG_SIZE', 10 * 1024 * 1024)
)  # 10 MB
_MAX_LOG_FILES = int(os.getenv('PYSHARED_MAX_LOG_FILES', 5))
_FILE_LOGGING_ENABLED = os.getenv(
    'PYSHARED_FILE_LOGGING_ENABLED', 'True'
).lower() in ('true', '1', 'yes')

# Private global default logger instance
_default_logger = None


def get_logger(
    name: str = _LOG_NAME, level: Opt[str] = None, log_file: Opt[str] = None
):

    global _default_logger
    if name == _LOG_NAME and _default_logger is not None:
        return _default_logger

    log_level = level if level is not None else _LOG_LEVEL
    file_path = log_file if log_file is not None else _LOG_FILE

    # Configure a new logger or the default one
    logger = getLogger(name)
    logger.setLevel(log_level)
    logger.handlers = []  # Clear existing handlers to prevent duplicate logs

    # Console Handler
    console_handler = StreamHandler()
    console_handler.setLevel(log_level)
    console_format = Formatter(_LOG_FORMAT, _DATE_FORMAT)
    console_handler.setFormatter(console_format)
    logger.addHandler(console_handler)

    # File Handler
    if _FILE_LOGGING_ENABLED:
        file_handler = RotatingFileHandler(
            file_path, maxBytes=_MAX_LOG_SIZE, backupCount=_MAX_LOG_FILES
        )
        file_handler.setLevel(log_level)
        file_format = Formatter(_LOG_FORMAT, _DATE_FORMAT)
        file_handler.setFormatter(file_format)
        logger.addHandler(file_handler)

    if name == _LOG_NAME:
        _default_logger = logger

    return logger
