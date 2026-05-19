"""
Tests for shared utilities.
"""

from src.shared.config_loader import ConfigLoader


def test_load_json():
    """
    Test JSON config loading.
    """

    config = ConfigLoader.load_json(
        "config/setup.json"
    )

    assert config["version"] == "1.00"