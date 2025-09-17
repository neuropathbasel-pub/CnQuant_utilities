import sys

sys.path.insert(0, "../..")
sys.path.insert(0, "../CnQuant_utilities")
import unittest
import logging
import tempfile
import os
from pathlib import Path
from unittest.mock import patch, MagicMock
from CnQuant_utilities.logger import Logger, AsyncLogger


class TestLogger(unittest.TestCase):
    def setUp(self):
        self.logger_name = f"test_logger_{self._testMethodName}"
        self.temp_log_file = tempfile.NamedTemporaryFile(delete=False)
        self.temp_log_file.close()

    def tearDown(self):
        if os.path.exists(self.temp_log_file.name):
            os.unlink(self.temp_log_file.name)

    def test_init_valid_levels(self):
        logger_instance = Logger(
            name=self.logger_name, log_level="info", file_log_level="error"
        )
        self.assertEqual(logger_instance.logger.name, self.logger_name)
        self.assertEqual(logger_instance.logger.level, logging.INFO)

    def test_init_invalid_log_level(self):
        with self.assertRaises(ValueError):
            Logger(name=self.logger_name, log_level="invalid")

    def test_init_invalid_file_log_level(self):
        with self.assertRaises(ValueError):
            Logger(name=self.logger_name, file_log_level="invalid")

    def test_console_handler_setup(self):
        logger_instance = Logger(name=self.logger_name)
        handlers = logger_instance.logger.handlers
        self.assertEqual(len(handlers), 1)
        self.assertIsInstance(handlers[0], logging.StreamHandler)

    def test_file_handler_setup(self):
        logger_instance = Logger(
            name=self.logger_name, log_file=self.temp_log_file.name
        )
        handlers = logger_instance.logger.handlers
        self.assertEqual(len(handlers), 2)  # Console + File
        self.assertIsInstance(handlers[1], logging.FileHandler)

    @patch("CnQuant_utilities.logger.SMTPHandler")
    def test_email_handler_setup(self, mock_smtp):
        logger_instance = Logger(
            name=self.logger_name,
            smtp_user="user@example.com",
            smtp_host="smtp.example.com",
            smtp_password="password",
            email_to="to@example.com",
            log_level="critical",
        )
        handlers = logger_instance.logger.handlers
        self.assertEqual(len(handlers), 2)  # Console + Email
        mock_smtp.assert_called_once()

    def test_get_logger(self):
        logger_instance = Logger(name=self.logger_name)
        retrieved_logger = logger_instance.get_logger()
        self.assertEqual(retrieved_logger, logger_instance.logger)


class TestAsyncLogger(unittest.TestCase):
    def setUp(self):
        self.logger_name = f"test_async_logger_{self._testMethodName}"
        self.temp_log_file = tempfile.NamedTemporaryFile(delete=False)
        self.temp_log_file.close()

    def tearDown(self):
        if os.path.exists(self.temp_log_file.name):
            os.unlink(self.temp_log_file.name)

    def test_init_valid_levels(self):
        logger_instance = AsyncLogger(
            name=self.logger_name, log_level="info", file_log_level="error"
        )
        self.assertEqual(logger_instance.logger.name, self.logger_name)
        self.assertEqual(logger_instance.logger.level, logging.INFO)

    def test_init_invalid_log_level(self):
        with self.assertRaises(ValueError):
            AsyncLogger(name=self.logger_name, log_level="invalid")

    def test_console_handler_setup(self):
        logger_instance = AsyncLogger(name=self.logger_name)
        handlers = logger_instance.logger.handlers
        self.assertEqual(len(handlers), 1)
        self.assertIsInstance(handlers[0], logging.handlers.QueueHandler)  # type: ignore

    def test_file_handler_setup(self):
        logger_instance = AsyncLogger(
            name=self.logger_name, log_file=self.temp_log_file.name
        )
        handlers = logger_instance.logger.handlers
        self.assertEqual(len(handlers), 1)  # Only the QueueHandler is added to the logger
        self.assertIsInstance(handlers[0], logging.handlers.QueueHandler)  # type: ignore

    @patch("CnQuant_utilities.logger.SMTPHandler")
    def test_email_handler_setup(self, mock_smtp):
        logger_instance = AsyncLogger(
            name=self.logger_name,
            smtp_user="user@example.com",
            smtp_host="smtp.example.com",
            smtp_password="password",
            email_to="to@example.com",
            log_level="critical",
        )
        handlers = logger_instance.logger.handlers
        self.assertEqual(len(handlers), 2)  # Main QueueHandler + Email QueueHandler
        mock_smtp.assert_called_once()

    def test_start_stop_async_logging(self):
        logger_instance = AsyncLogger(name=self.logger_name)
        logger_instance.start_async_logging()
        self.assertTrue(
            all(
                hasattr(listener, "_thread")
                and listener._thread
                and listener._thread.is_alive()
                for listener in logger_instance.listeners
            )
        )
        logger_instance.stop_async_logging()
        self.assertTrue(
            all(
                not (
                    hasattr(listener, "_thread")
                    and listener._thread
                    and listener._thread.is_alive()
                )
                for listener in logger_instance.listeners
            )
        )

    def test_get_logger(self):
        logger_instance = AsyncLogger(name=self.logger_name)
        retrieved_logger = logger_instance.get_logger()
        self.assertEqual(retrieved_logger, logger_instance.logger)


class TestFormatter(unittest.TestCase):
    def test_format_info(self):
        formatter = logging.Formatter(fmt="%(levelname)s - %(message)s")
        record = logging.LogRecord(
            name="test",
            level=logging.INFO,
            pathname="",
            lineno=0,
            msg="Test message",
            args=(),
            exc_info=None,
        )
        formatted = formatter.format(record)
        self.assertIn("INFO", formatted)  # Check for level name

    def test_format_warning(self):
        formatter = logging.Formatter(fmt="%(levelname)s - %(message)s")
        record = logging.LogRecord(
            name="test",
            level=logging.WARNING,
            pathname="",
            lineno=0,
            msg="Test message",
            args=(),
            exc_info=None,
        )
        formatted = formatter.format(record)
        self.assertIn("WARNING", formatted)  # Check for level name

    def test_format_error(self):
        formatter = logging.Formatter(fmt="%(levelname)s - %(message)s")
        record = logging.LogRecord(
            name="test",
            level=logging.ERROR,
            pathname="",
            lineno=0,
            msg="Test message",
            args=(),
            exc_info=None,
        )
        formatted = formatter.format(record)
        self.assertIn("ERROR", formatted)

if __name__ == "__main__":
    unittest.main()