"""
Tests for the Debate Orchestrator and Watchdog logic with memory updates.
"""

import os

# Inject a fake key so the Gatekeeper doesn't crash during test initialization
os.environ["GEMINI_API_KEY"] = "dummy_test_key"

from unittest.mock import patch, MagicMock
from src.services.orchestrator import DebateOrchestrator

@patch("src.services.agents.ProAgent.update_memory")
@patch("src.services.agents.ConAgent.update_memory")
@patch("src.services.agents.ProAgent.generate_response")
@patch("src.services.agents.ConAgent.generate_response")
@patch("src.services.orchestrator.ApiGatekeeper")
def test_orchestrator_loop_and_verdict(mock_gatekeeper_class, mock_con_gen, mock_pro_gen, mock_con_mem, mock_pro_mem):
    """Test that the orchestrator loops correctly and writes the final decision."""

    # Mock the judge's gatekeeper to prevent live final verdict generation
    gatekeeper_instance = MagicMock()
    gatekeeper_instance.generate_response.return_value = "WINNER: PRO. Grades: Pro 95, Con 80."
    mock_gatekeeper_class.return_value = gatekeeper_instance

    # Mock the agents' generate_response methods to return strict valid JSON
    valid_response = {
        "thought_process": "thinking",
        "argument_summary": "summary",
        "full_argument": "This is a valid short argument.",
        "addressed_opponent_points": ["point 1"],
        "sources_used": []
    }
    mock_pro_gen.return_value = valid_response
    mock_con_gen.return_value = valid_response

    # Mock the subagent memory compression to avoid live API calls
    mock_pro_mem.return_value = {"my_arguments": []}
    mock_con_mem.return_value = {"my_arguments": []}

    # Initialize and run a shortened 1-round debate
    orchestrator = DebateOrchestrator()
    orchestrator.gatekeeper = gatekeeper_instance
    
    orchestrator.initialize_debate("Cats vs Dogs")
    orchestrator.total_rounds = 1
    orchestrator.run_debate_loop()

    # Assertions
    assert mock_pro_gen.call_count >= 1
    assert mock_con_gen.call_count >= 1
    assert os.path.exists("data/results/final_decision.md")


def test_word_count_validator_watchdog():
    """Test that the Judge correctly flags and rejects arguments over 100 words."""

    # Patch the Gatekeeper inside this test to avoid live API calls
    with patch("src.services.agents.ApiGatekeeper"):
        orchestrator = DebateOrchestrator()

        # Generate an argument exactly 101 words long
        long_text = "word " * 101
        mock_response = {
            "full_argument": long_text.strip(),
            "addressed_opponent_points": ["point"]
        }

        is_valid, error_msg = orchestrator._validate_argument(mock_response)

        assert not is_valid
        assert "exceeding the maximum allowed limit of 100 words" in error_msg