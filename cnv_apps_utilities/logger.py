import logging
import os
from logging.handlers import SMTPHandler
from pathlib import Path

class Logger:
    def __init__(
        self,
        name: str,
        log_file: str | Path | None = None,
        file_log_level: str | None = "none",
        log_level: str = "info",
        smtp_user: str = "",
        smtp_host: str = "",
        smtp_password: str = "",
        email_to: str = "",
        email_subject: str = "",
        smtp_port: int = 587,
        log_level_for_emails: str = "critical"
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
        self.log_level = log_level.lower()
        self.log_level_for_emails: str = log_level_for_emails
        self.file_log_level: str = file_log_level.lower() if file_log_level is not None else "none"
        self.log_levels: list[str] = ["none", "debug", "info", "warning", "error", "critical"]

        if self.log_level not in self.log_levels:
             raise ValueError(f"log_level has to be one of the following: {','.join(self.log_levels)}. Provided option was {log_level}")
        
        if self.file_log_level not in self.log_levels:
            raise ValueError(f"log_level has to be one of the following: {','.join(self.log_levels)}. Provided option was {file_log_level}")
        
        # Select log level
        self.logger.setLevel(level=logging.INFO)  

        # Console log level
        if self.log_level == "info":
             console_log_level = logging.INFO
        elif self.log_level == "warning":
             console_log_level = logging.WARNING
        elif self.log_level == "error":
             console_log_level = logging.ERROR
        elif self.log_level == "critical":
            console_log_level = logging.CRITICAL
        elif self.log_level == "debug":
            console_log_level = logging.DEBUG
        else:
            console_log_level = logging.NOTSET
        

        # File log level
        if self.file_log_level == "info":
            _file_log_level = logging.INFO
        elif self.file_log_level == "warning":
            _file_log_level = logging.WARNING
        elif self.file_log_level == "error":
            _file_log_level = logging.ERROR
        elif self.file_log_level == "critical":
            _file_log_level = logging.CRITICAL
        elif self.file_log_level == "debug":
            _file_log_level = logging.DEBUG
        else:
            _file_log_level = logging.NOTSET      

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
                log_file = str(object=log_file)
                os.makedirs(name=os.path.dirname(p=log_file), exist_ok=True)
                file_handler = logging.FileHandler(filename=log_file)
                # Select level on which the messages will be saved to a file
                file_handler.setLevel(level=_file_log_level)
                
                file_format = logging.Formatter(
                    fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
                )
                file_handler.setFormatter(fmt=file_format)
                self.logger.addHandler(hdlr=file_handler)

            # Email handler for CRITICAL
            if all([smtp_user, smtp_host, smtp_password, email_to]) and self.log_level == self.log_level_for_emails:
                email_handler = SMTPHandler(
                    mailhost=(smtp_host, smtp_port),
                    fromaddr=smtp_user,
                    toaddrs=email_to,
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