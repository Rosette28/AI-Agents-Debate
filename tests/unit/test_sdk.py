"""
Tests for the public SDK Entry Point.
"""

import sys
from unittest.mock import patch, MagicMock
import pytest

# Dynamically fake the missing orchestrator module structure in sys.modules 
# so the inline import inside sdk.py doesn't crash during Phase 3 testing.
mock_orch_module = MagicMock()
sys.modules["src.services.orchestrator"] = mock_orch_module

from src.sdk.sdk import DebateSDK


@patch("src.services.orchestrator.DebateOrchestrator", create=True)
def test_sdk_delegates_to_orchestrator(mock_orchestrator_class):
    """Test that the SDK cleanly initializes and delegates calls to the Orchestrator."""
    # Setup mocks
    mock_orch_instance = MagicMock()
    mock_orchestrator_class.return_value = mock_orch_instance
    mock_orch_module.DebateOrchestrator = mock_orchestrator_class

    # Initialize SDK
    sdk = DebateSDK()

    # Configure debate
    sdk.configure_debate("Cats vs Dogs")
    assert sdk.topic == "Cats vs Dogs"

    # Run debate
    sdk.run_debate()
    mock_orch_instance.initialize_debate.assert_called_once_with("Cats vs Dogs")
    mock_orch_instance.run_debate_loop.assert_called_once()