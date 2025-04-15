import logging
import os
from logging.handlers import SMTPHandler
from pathlib import Path

class Logger:
    def __init__(
        self,
        name: str,
        log_file: str | Path,
        log_level: int = logging.INFO,
        smtp_user: str = "",
        smtp_host: str = "",
        smtp_password: str = "",
        email_to: str = "",
        email_subject: str = "",
        smtp_port: int = 587,
    ):
        """
        # TODO: test it extensively. Add checking for separator in email_to
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
        self.logger.setLevel(level=log_level)

        # Avoid duplicate handlers if logger is reused
        if not self.logger.handlers:
            # Console handler
            console_handler = logging.StreamHandler()
            console_handler.setLevel(level=log_level)
            console_format = logging.Formatter(
                fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            )
            console_handler.setFormatter(fmt=console_format)
            self.logger.addHandler(hdlr=console_handler)

            # File handler
            os.makedirs(name=os.path.dirname(p=log_file), exist_ok=True)
            file_handler = logging.FileHandler(filename=log_file)
            file_handler.setLevel(level=log_level)
            file_format = logging.Formatter(
                fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            )
            file_handler.setFormatter(fmt=file_format)
            self.logger.addHandler(hdlr=file_handler)

            # Email handler for CRITICAL
            if all([smtp_user, smtp_host, smtp_password, email_to]):
                email_handler = SMTPHandler(
                    mailhost=(smtp_host, smtp_port),
                    fromaddr=smtp_user,
                    toaddrs=email_to.split(sep=","),
                    subject=email_subject,
                    credentials=(smtp_user, smtp_password),
                    secure=()
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