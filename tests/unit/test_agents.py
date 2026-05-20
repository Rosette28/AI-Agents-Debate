"""
Tests for Concrete Agent Definitions and JSON Enforcement.
"""

from unittest.mock import patch, MagicMock
from src.services.agents import BaseAgent, ProAgent, ConAgent

@patch("src.services.agents.ApiGatekeeper")
@patch("src.services.agents.ConfigLoader.load_json")
def test_base_agent_enforces_json(mock_load_json, mock_gatekeeper_class):
    """Test that BaseAgent forces a valid JSON return and parses it."""
    # Mock the prompt config
    mock_load_json.return_value = {
        "test_role": {"system_instruction": "Be smart", "response_guidelines": "Return JSON"}
    }

    # Mock the LLM returning a stringified JSON
    mock_gatekeeper = MagicMock()
    mock_gatekeeper.generate_response.return_value = '{"thought_process": "thinking", "argument_summary": "summary", "full_argument": "argument", "addressed_opponent_points": [], "sources_used": []}'
    mock_gatekeeper_class.return_value = mock_gatekeeper

    # Initialize agent and generate response
    agent = BaseAgent("test_role")
    response = agent.generate_response("AI Topic", "Opponent said this", {})

    # Verify it parsed it into a real Python dictionary
    assert type(response) is dict
    assert response["full_argument"] == "argument"
    mock_gatekeeper.generate_response.assert_called_once()

@patch("src.services.agents.ApiGatekeeper")
@patch("src.services.agents.ConfigLoader.load_json")
def test_pro_agent(mock_load_json, mock_gatekeeper_class):
    """Test ProAgent."""
    # Mock the config load specifically for the Pro agent
    mock_load_json.return_value = {
        "pro_agent": {"system_instruction": "PRO", "response_guidelines": ""}
    }

    # Mock the Gatekeeper returning JSON
    mock_gatekeeper = MagicMock()
    mock_gatekeeper.generate_response.return_value = '{"full_argument": "AI is beneficial"}'
    mock_gatekeeper_class.return_value = mock_gatekeeper

    agent = ProAgent()

    # The new generate_response takes topic, opponent_argument, and memory_state
    response = agent.generate_response(
        topic="AI", 
        opponent_argument="", 
        memory_state={}
    )

    assert response["full_argument"] == "AI is beneficial"
    assert agent.role_key == "pro_agent"

@patch("src.services.agents.ApiGatekeeper")
@patch("src.services.agents.ConfigLoader.load_json")
def test_con_agent(mock_load_json, mock_gatekeeper_class):
    """Test ConAgent."""
    # Mock the config load specifically for the Con agent
    mock_load_json.return_value = {
        "con_agent": {"system_instruction": "CON", "response_guidelines": ""}
    }

    # Mock the Gatekeeper returning JSON
    mock_gatekeeper = MagicMock()
    mock_gatekeeper.generate_response.return_value = '{"full_argument": "AI is dangerous"}'
    mock_gatekeeper_class.return_value = mock_gatekeeper

    agent = ConAgent()

    # The new generate_response takes topic, opponent_argument, and memory_state
    response = agent.generate_response(
        topic="AI", 
        opponent_argument="", 
        memory_state={}
    )

    assert response["full_argument"] == "AI is dangerous"
    assert agent.role_key == "con_agent"