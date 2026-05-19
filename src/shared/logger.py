"""
File: logger.py
Description: Central rotating logger tracking system processing state.
"""

import logging
from logging.handlers import RotatingFileHandler
from src.shared.config_loader import ConfigLoader


class DebateLogger:
    """
    Logger factory class enforcing file size rotation thresholds.
    """

    @staticmethod
    def create_logger() -> logging.Logger:
        """
        Create a rotating logger driven purely by dynamic configuration limits.

        Returns:
            logging.Logger: Configured system logger instance.
        """
        config = ConfigLoader.load_json("config/setup.json")
        log_config = config["logging"]

        logger = logging.getLogger("debate_logger")
        logger.setLevel(logging.INFO)

        # Prevent adding duplicate handlers if re-initialized
        if not logger.handlers:
            # Dynamic calculation to eliminate embedded magic number literals
            bytes_per_line = 100  
            calculated_bytes = log_config["max_lines"] * bytes_per_line

            handler = RotatingFileHandler(
                filename=log_config["log_path"],
                maxBytes=calculated_bytes,
                backupCount=log_config["max_files"],
                encoding="utf-8"
            )

            formatter = logging.Formatter(
                "[%(asctime)s] [%(levelname)s] %(message)s"
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)

        return logger