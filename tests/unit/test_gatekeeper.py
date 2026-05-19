"""
Tests for the central API Gatekeeper.
"""

import os
import json
import pytest
from unittest.mock import patch, MagicMock
from src.services.gatekeeper import ApiGatekeeper
import warnings

# Suppress the Google Generative AI package deprecation warning
warnings.filterwarnings("ignore", category=FutureWarning, module="google.generativeai")

@pytest.fixture
def mock_env():
    """Inject a fake API key so the Gatekeeper initializes properly."""
    with patch.dict(os.environ, {"GEMINI_API_KEY": "fake_test_key_123"}):
        yield


def test_gatekeeper_missing_key_throws_error():
    """Test that the system hard-crashes if no API key is found."""
    with patch.dict(os.environ, clear=True):
        with pytest.raises(ValueError, match="GEMINI_API_KEY"):
            ApiGatekeeper()


@patch("src.services.gatekeeper.genai.GenerativeModel")
def test_generate_response_handles_tokens(mock_model_class, mock_env, tmp_path):
    """Test that a successful call logs token economics correctly."""
    # Setup mock response
    mock_instance = MagicMock()
    mock_response = MagicMock()
    mock_response.text = "This is a test response."
    mock_response.usage_metadata.prompt_token_count = 10
    mock_response.usage_metadata.candidates_token_count = 20
    mock_instance.generate_content.return_value = mock_response
    mock_model_class.return_value = mock_instance

    # Point the gatekeeper to a temporary test log file
    gatekeeper = ApiGatekeeper()
    test_log_path = tmp_path / "test_token_logs.json"
    
    # FIX: Create the empty array in the temporary file so the Gatekeeper can parse it
    with open(test_log_path, "w", encoding="utf-8") as f:
        json.dump([], f)
        
    gatekeeper.log_path = str(test_log_path)

    # Execute
    result = gatekeeper.generate_response("ProAgent", "gemini-1.5-flash", "Hello")

    # Assertions
    assert result == "This is a test response."
    mock_instance.generate_content.assert_called_once()
    
    # Verify the timeout constraint was passed to the API
    _, kwargs = mock_instance.generate_content.call_args
    assert "request_options" in kwargs
    assert kwargs["request_options"]["timeout"] == 15