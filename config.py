from pathlib import Path
from cnv_apps_utilities.logger_setup import setup_logger, log_error

setup_logger(log_directory=Path("/home/ben/dev/CNV_apps_utilities"), log_file_name="test.log")



my_logger = setup_logger(log_directory=Path("/home/ben/dev/CNV_apps_utilities"), log_file_name="test.log")
