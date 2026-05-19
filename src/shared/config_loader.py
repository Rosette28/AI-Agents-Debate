"""
File: config_loader.py
Description: Loads and validates JSON configuration files.
"""

import json


class ConfigLoader:
    """
    Utility class for loading configuration maps securely.
    """

    @staticmethod
    def load_json(path: str) -> dict:
        """
        Load a JSON configuration file and enforce version compatibility.

        Args:
            path (str): File path location.

        Returns:
            dict: Evaluated configuration data.
        """
        with open(path, "r", encoding="utf-8") as file:
            data = json.load(file)

        # Enforce Dr. Segal's Mandatory Startup Version Check
        if "version" in data and data["version"] != "1.00":
            raise ValueError(
                f"Configuration version mismatch in {path}. Expected 1.00"
            )

        return data