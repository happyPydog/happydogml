import logging

from happydogml.logging import get_logger


def test_get_logger_single_instance():
    logger1 = get_logger("test_logger")
    logger2 = get_logger("test_logger")
    assert logger1 is logger2


def test_get_logger_configuration():
    logger = get_logger("configured_logger", level="DEBUG")
    assert logger.level == logging.DEBUG
    assert not logger.propagate
    assert len(logger.handlers) == 1
    assert hasattr(
        logger.handlers[0], "console"
    ), "Handler should be a RichHandler"


def test_logger_thread_safety():
    import threading

    loggers = []

    def get_logger_thread():
        logger = get_logger("thread_safe_logger")
        loggers.append(logger)

    threads = [threading.Thread(target=get_logger_thread) for _ in range(10)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

    for logger in loggers[1:]:
        assert loggers[0] is logger
