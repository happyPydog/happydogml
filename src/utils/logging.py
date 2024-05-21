""" Logging utilities.

Here are some good reference source for writing custom loggers:
- Python Logging howto:
    https://docs.python.org/3/howto/logging.html
- jamesmurphy-mc tutorial:
    https://github.com/mCodingLLC/VideosSampleCode/tree/master/videos/135_modern_logging

"""

import os
import sys
import json
import logging
import logging.config
import threading
import typing as t
import datetime as dt

_lock = threading.Lock()
_default_handler: t.Optional[logging.Handler] = None
_default_logging_level = logging.INFO


def _get_library_name() -> str:
    return __name__.split(".")[0]


class JSONFormatter(logging.Formatter):
    def __init__(
        self,
        *,
        fmt_keys: dict[str, str] | None = None,
    ):
        super().__init__()
        self.fmt_keys = fmt_keys if fmt_keys is not None else {}

    def format(self, record: logging.LogRecord) -> str:
        message = self._prepare_log_dict(record)
        return json.dumps(message, default=str)

    def _prepare_log_dict(self, record: logging.LogRecord):
        always_fields = {
            "message": record.getMessage(),
            "timestamp": dt.datetime.fromtimestamp(
                record.created, tz=dt.timezone.utc
            ).isoformat(),
        }
        if record.exc_info is not None:
            always_fields["exc_info"] = self.formatException(record.exc_info)

        if record.stack_info is not None:
            always_fields["stack_info"] = self.formatStack(record.stack_info)

        message = {
            key: (
                msg_val
                if (msg_val := always_fields.pop(val, None)) is not None
                else getattr(record, val)
            )
            for key, val in self.fmt_keys.items()
        }
        message.update(always_fields)
        return message


def _config_root_logger(logger: logging.Logger) -> None:
    global _default_handler
    with _lock:
        if _default_handler:
            # * This library has already configured the library root logger.
            return
        if sys.stderr is None:
            sys.stderr = open(os.devnull, "w")

        _default_handler = logging.StreamHandler()
        _default_handler.flush = sys.stderr.flush
        _default_formatter = JSONFormatter()
        _default_handler.setFormatter(_default_formatter)

        logger.addHandler(_default_handler)
        logger.setLevel(_default_logging_level)


def get_logger(name: t.Optional[str] = None) -> logging.Logger:
    if name is None:
        name = _get_library_name()

    logger = logging.getLogger(name)
    _config_root_logger(logger)
    return logger
