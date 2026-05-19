"""
Tests for shared configuration loading and system logging utilities.
"""

import pytest
from src.shared.config_loader import ConfigLoader


def test_load_json_success():
    """Test successful configuration file processing parsing rules."""
    config = ConfigLoader.load_json("config/setup.json")
    assert config["version"] == "1.00"
    assert config["max_rounds"] == 10


def test_load_json_missing_file_throws_error():
    """Test that missing path variables accurately raise a FileNotFoundError."""
    with pytest.raises(FileNotFoundError):
        ConfigLoader.load_json("config/non_existent_file.json")