import inspect
import sys
import time
from pathlib import Path

from loguru import logger as log
import logging

from core.config import settings

# Переменная для установки уровня логирования
# CRITICAL = 50
# FATAL = CRITICAL
# ERROR = 40
# WARNING = 30
# WARN = WARNING
# INFO = 20
# DEBUG = 10
# NOTSET = 0
log_level = settings.log_level


class InterceptHandler(logging.Handler):
    def emit(self, record: logging.LogRecord) -> None:
        # Get corresponding Loguru level if it exists.
        level: str | int
        try:
            level = log.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # Find caller from where originated the logged message.
        frame, depth = inspect.currentframe(), 0
        while frame and (depth == 0 or frame.f_code.co_filename == logging.__file__):
            frame = frame.f_back
            depth += 1

        log.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())


def configure_logging(logging, level: int = log_level, log_file: str | Path = None):
    # Удаляем существующие обработчики, чтобы избежать дублирования
    logging.getLogger().handlers = []

    if log_file is not None:
        if isinstance(log_file, str):
            log_file = settings.log_dir / log_file
        log.add(log_file)  # , level=level, format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level} | {name}:{line} - {message}"

    logging.Formatter.converter = time.gmtime  # date time in GMT/UTC
    logging.basicConfig(
        handlers=[InterceptHandler()],
        level=level,
        # force=True,
        format="[%(asctime)s.%(msecs)03d] %(funcName)20s %(module)s:%(lineno)d %(levelname)-8s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    return logging.getLogger(__name__)


# Конфигурируем логирование при импорте модуля
logger = configure_logging(logging, log_file='default.log')
