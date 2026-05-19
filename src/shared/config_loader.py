"""
File: config_loader.py
Description:
Loads JSON configuration files.
"""

import json


class ConfigLoader:
    """
    Utility class for loading JSON files.
    """

    @staticmethod
    def load_json(path):
        """
        Load JSON file.

        Args:
            path (str): File path.

        Returns:
            dict: Parsed JSON data.
        """

        with open(path, "r") as file:
            return json.load(file)