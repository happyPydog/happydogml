import unittest
import logging
import io

from src.utils.logging import get_logger, JSONFormatter


class TestLogger(unittest.TestCase):
    def setUp(self):
        self.logger = get_logger("test_logger")
        self.log_capture_string = io.StringIO()
        self.stream_handler = logging.StreamHandler(self.log_capture_string)
        self.stream_handler.setFormatter(JSONFormatter())
        self.logger.addHandler(self.stream_handler)
        self.logger.setLevel(logging.INFO)

    def tearDown(self):
        self.logger.removeHandler(self.stream_handler)

    def test_base_logging_output(self):
        test_log = {
            "msg": "test_message",
            "funcName": "test_function",
        }
        with self.assertLogs() as cm:
            self.logger.info(test_log)

        self.assertIn("msg", cm.output[0])
        self.assertIn("funcName", cm.output[0])

        logged_output = self.log_capture_string.getvalue()
        self.assertIn("msg", logged_output)
        self.assertIn("funcName", logged_output)
        self.assertIn("timestamp", logged_output)

    def test_logging_levels(self):
        self.logger.setLevel(logging.DEBUG)
        test_log = {
            "msg": "test_message_debug",
            "funcName": "test_function_debug",
        }
        with self.assertLogs(level="DEBUG") as cm:
            self.logger.debug(test_log)

        self.assertIn("msg", cm.output[0])
        self.assertIn("funcName", cm.output[0])

        logged_output = self.log_capture_string.getvalue()
        self.assertIn("msg", logged_output)
        self.assertIn("funcName", logged_output)
        self.assertIn("timestamp", logged_output)

    def test_exception_logging(self):
        try:
            # Code that may raise an exception
            raise ValueError("Test exception")
        except ValueError:
            self.logger.exception("Exception occurred")

        logged_output = self.log_capture_string.getvalue()
        self.assertIn("Exception occurred", logged_output)
        self.assertIn("ValueError: Test exception", logged_output)
        self.assertIn("timestamp", logged_output)
