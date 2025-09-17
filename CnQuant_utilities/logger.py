import logging
import orjson
from logging.handlers import SMTPHandler, QueueHandler, QueueListener
from datetime import datetime
from queue import Queue
from pathlib import Path


class JsonFormatter(logging.Formatter):
    def format(self, record):
        # Format time as ISO 8601
        time_str = datetime.fromtimestamp(record.created).isoformat()
        
        log_entry = {
            "time": time_str,
            "level": record.levelname,
            "message": record.getMessage()
        }
        return orjson.dumps(log_entry)


class AsyncLogger:
    LOG_LEVEL_MAP = {
        "debug": logging.DEBUG,
        "info": logging.INFO,
        "warning": logging.WARNING,
        "error": logging.ERROR,
        "critical": logging.CRITICAL,
        "none": logging.NOTSET,
    }

    def __init__(
        self,
        name: str,
        log_file: str | Path | None = None,
        file_log_level: str = "info",
        log_level: str = "info",
        smtp_user: str = "",
        smtp_host: str = "",
        smtp_password: str = "",
        email_to: str = "",
        email_subject: str = "",
        smtp_port: int = 587,
        log_level_for_emails: str = "critical",
    ):
        """
        Initialize a logger with console, file, and email handlers.

        Args:
            name: Logger name (e.g., module name).
            log_file: Path to log file (e.g., '/app/logs/app.log').
            log_level: Logging level (e.g., logging.INFO).
            smtp_host: SMTP server host.
            smtp_port: SMTP server port.
            smtp_user: SMTP username (email).
            smtp_password: SMTP password.
            email_to: Comma-separated list as a string of recipient email addresses for critical logs.
            email_subject: Subject for critical log emails.
        """
        self.logger = logging.getLogger(name=name)
        self.log_level = log_level.lower()
        self.log_level_for_emails: str = log_level_for_emails
        self.file_log_level: str = (
            file_log_level.lower() if file_log_level is not None else "none"
        )
        self.queue = Queue()
        self.listeners = []
        handlers = []
        if self.log_level not in self.LOG_LEVEL_MAP:
            raise ValueError(
                f"log_level must be one of: {', '.join(self.LOG_LEVEL_MAP.keys())}. Got: {self.log_level}"
            )

        if self.file_log_level not in self.LOG_LEVEL_MAP:
            raise ValueError(
                f"file_log_level must be one of: {', '.join(self.LOG_LEVEL_MAP.keys())}. Got: {self.file_log_level}"
            )

        console_log_level = self.LOG_LEVEL_MAP[self.log_level]
        _file_log_level = self.LOG_LEVEL_MAP[self.file_log_level]

        # Select log level
        min_level = min(
            console_log_level, _file_log_level if log_file else logging.CRITICAL
        )
        self.logger.setLevel(level=min_level)

        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(level=console_log_level)
        console_format = logging.Formatter(
            fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        console_handler.setFormatter(fmt=console_format)
        handlers.append(console_handler)

        # File handler
        if log_file is not None:
            log_file_path = Path(log_file)
            log_file_path.parent.mkdir(parents=True, exist_ok=True)
            file_handler = logging.FileHandler(filename=log_file_path, mode='ab')
            file_handler.setLevel(level=_file_log_level)
            file_format = JsonFormatter()
            file_handler.setFormatter(fmt=file_format)
            file_handler.terminator = b'\n'  # type: ignore
            handlers.append(file_handler)

        # Email handler (async)
        if (
            all([smtp_user, smtp_host, smtp_password, email_to])
            and self.log_level == self.log_level_for_emails
        ):
            try:
                email_handler = SMTPHandler(
                    mailhost=(smtp_host, smtp_port),
                    fromaddr=smtp_user,
                    toaddrs=email_to.split(","),
                    subject=email_subject,
                    credentials=(smtp_user, smtp_password),
                    secure=(),
                )
                email_handler.setLevel(level=logging.CRITICAL)
                email_format = logging.Formatter(
                    fmt="%(asctime)s - %(name)s - %(levelname)s\n%(pathname)s:%(lineno)d"
                )
                email_handler.setFormatter(fmt=email_format)
                queue_email_handler = QueueHandler(queue=self.queue)
                self.listeners.append(QueueListener(self.queue, email_handler))
                self.logger.addHandler(hdlr=queue_email_handler)
            except Exception as e:
                self.logger.warning(f"Failed to set up email handler: {e}")

        # Use one listener for all handlers
        if handlers:
            queue_handler = QueueHandler(self.queue)
            self.logger.addHandler(queue_handler)
            self.listeners.append(QueueListener(self.queue, *handlers))

        # Set logger level
        if handlers:
            handler_levels = [h.level for h in handlers]
            min_level = min(handler_levels) if handler_levels else logging.DEBUG
            self.logger.setLevel(min_level)

    def start_async_logging(self):
        """Start the asynchronous listeners."""
        for listener in self.listeners:
            listener.start()

    def stop_async_logging(self):
        """Stop the asynchronous listeners."""
        for listener in self.listeners:
            listener.stop()

    def get_logger(self) -> logging.Logger:
        """Return the configured logger."""
        return self.logger


class Logger:
    LOG_LEVEL_MAP = {
        "debug": logging.DEBUG,
        "info": logging.INFO,
        "warning": logging.WARNING,
        "error": logging.ERROR,
        "critical": logging.CRITICAL,
        "none": logging.NOTSET,
    }

    def __init__(
        self,
        name: str,
        log_file: str | Path | None = None,
        file_log_level: str | None = "error",
        log_level: str = "info",
        smtp_user: str = "",
        smtp_host: str = "",
        smtp_password: str = "",
        email_to: str = "",
        email_subject: str = "",
        smtp_port: int = 587,
        log_level_for_emails: str = "critical",
    ):
        """
        Initialize a logger with console, file, and email handlers.

        Args:
            name: Logger name (e.g., module name).
            log_file: Path to log file (e.g., '/app/logs/app.log').
            log_level: Logging level (e.g., logging.INFO).
            smtp_host: SMTP server host.
            smtp_port: SMTP server port.
            smtp_user: SMTP username (email).
            smtp_password: SMTP password.
            email_to: Comma-separated list as a string of recipient email addresses for critical logs.
            email_subject: Subject for critical log emails.
        """
        self.logger = logging.getLogger(name=name)
        self.log_level = log_level.lower()
        self.log_level_for_emails: str = log_level_for_emails
        self.file_log_level: str = (
            file_log_level.lower() if file_log_level is not None else "none"
        )
        self.log_levels: list[str] = [
            "none",
            "debug",
            "info",
            "warning",
            "error",
            "critical",
        ]

        if self.log_level not in self.LOG_LEVEL_MAP:
            raise ValueError(
                f"log_level must be one of: {', '.join(self.LOG_LEVEL_MAP.keys())}. Got: {self.log_level}"
            )

        if self.file_log_level not in self.LOG_LEVEL_MAP:
            raise ValueError(
                f"file_log_level must be one of: {', '.join(self.LOG_LEVEL_MAP.keys())}. Got: {self.file_log_level}"
            )

        console_log_level = self.LOG_LEVEL_MAP[self.log_level]
        _file_log_level = self.LOG_LEVEL_MAP[self.file_log_level]

        # Select log level
        min_level = min(
            console_log_level, _file_log_level if log_file else logging.CRITICAL
        )
        self.logger.setLevel(level=min_level)

        # Avoid duplicate handlers if logger is reused
        if not self.logger.handlers:
            # Console handler
            console_handler = logging.StreamHandler()
            console_handler.setLevel(level=console_log_level)
            console_format = logging.Formatter(
                fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            )
            console_handler.setFormatter(fmt=console_format)
            self.logger.addHandler(hdlr=console_handler)

            # File handler
            if log_file is not None:
                log_file_path = Path(log_file)
                log_file_path.parent.mkdir(parents=True, exist_ok=True)
                file_handler = logging.FileHandler(filename=log_file_path)
                # Select level on which the messages will be saved to a file
                file_handler.setLevel(level=_file_log_level)

                file_format = logging.Formatter(
                    fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
                )
                file_handler.setFormatter(fmt=file_format)
                self.logger.addHandler(hdlr=file_handler)

            # Email handler for CRITICAL
            if (
                all([smtp_user, smtp_host, smtp_password, email_to])
                and self.log_level == self.log_level_for_emails
            ):
                email_handler = SMTPHandler(
                    mailhost=(smtp_host, smtp_port),
                    fromaddr=smtp_user,
                    toaddrs=email_to,
                    subject=email_subject,
                    credentials=(smtp_user, smtp_password),
                    secure=(),
                )
                email_handler.setLevel(level=logging.CRITICAL)
                email_format = logging.Formatter(
                    fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s\n%(pathname)s:%(lineno)d"
                )
                email_handler.setFormatter(fmt=email_format)
                self.logger.addHandler(hdlr=email_handler)

    def get_logger(self) -> logging.Logger:
        """Return the configured logger."""
        return self.logger


# class ColoredFormatter(logging.Formatter):
#     WHITE: str = "\033[97m"
#     GREEN: str = "\033[92m"
#     RED: str = "\033[91m"
#     BLUE: str = "\033[94m"
#     YELLOW: str = "\033[93m"
#     MAGENTA: str = "\033[95m"
#     CYAN: str = "\033[96m"
#     ORANGE: str = "\033[38;5;208m"
#     RESET: str = "\033[0m"

#     def format(self, record):
#         if record.levelno == logging.WARNING:
#             color = self.ORANGE
#         elif record.levelno in [logging.ERROR, logging.CRITICAL]:
#             color = self.RED
#         elif record.levelno == logging.INFO:
#             color = self.GREEN
#         else:
#             color = ""
#         record.msg = f"{color}{record.msg}{self.RESET}"
#         return super().format(record=record)
