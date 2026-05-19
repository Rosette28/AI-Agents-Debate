"""
File: logger.py
Description:
Central rotating logger for the debate system.
"""

import logging

from logging.handlers import RotatingFileHandler

from src.shared.config_loader import ConfigLoader


class DebateLogger:
    """
    Logger factory class.
    """

    @staticmethod
    def create_logger():
        """
        Create rotating logger.

        Returns:
            logging.Logger
        """

        config = ConfigLoader.load_json(
            "config/setup.json"
        )

        log_config = config["logging"]

        logger = logging.getLogger(
            "debate_logger"
        )

        logger.setLevel(logging.INFO)

        handler = RotatingFileHandler(
            filename=log_config["log_path"],
            maxBytes=500000,
            backupCount=log_config["max_files"]
        )

        formatter = logging.Formatter(
            "[%(asctime)s] [%(levelname)s] %(message)s"
        )

        handler.setFormatter(formatter)

        logger.addHandler(handler)

        return logger