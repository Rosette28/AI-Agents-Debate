"""
Tests for Advanced Reasoning Mixins (Skills).
"""

from unittest.mock import MagicMock
from src.services.agent_mixins import AdvancedReasoningMixin, ContextEngineeringMixin


class DummyAgent(AdvancedReasoningMixin, ContextEngineeringMixin):
    """A dummy agent to test mixin inheritance."""
    def __init__(self):
        self.gatekeeper = MagicMock()

# --- AdvancedReasoningMixin Tests ---

def test_fact_check_uses_live_search():
    agent = DummyAgent()
    agent.gatekeeper.generate_response.return_value = "[FALSE] The moon is rock. Source: nasa.gov"
    result = agent.fact_check("The moon is made of cheese")
    assert "[FALSE]" in result
    _, kwargs = agent.gatekeeper.generate_response.call_args
    assert kwargs.get("enable_search") is True

def test_find_new_arguments_two_step_process():
    agent = DummyAgent()
    agent.gatekeeper.generate_response.side_effect = ["Draft Argument 1", "Valid: Draft 1. Source: URL"]
    result = agent.look_for_arguments("AI", ["Old Arg 1"])
    assert "Valid:" in result
    assert agent.gatekeeper.generate_response.call_count == 2

def test_find_counterargument_fact_check_fails():
    agent = DummyAgent()
    agent.gatekeeper.generate_response.return_value = "[FALSE] That is incorrect."
    result = agent.find_counterarguments("Sky is green", [])
    assert "[FALSE]" in result
    assert agent.gatekeeper.generate_response.call_count == 1

def test_find_counterargument_not_found_searches_web():
    """Hits the branch where fact check is TRUE, memory is NOT_FOUND, triggering a web search."""
    agent = DummyAgent()
    agent.gatekeeper.generate_response.side_effect = [
        "[TRUE] The premise is factual.", 
        "[NOT_FOUND]", 
        "Web Search Counterargument"
    ]
    result = agent.find_counterarguments("Water is wet", ["Old arg"])
    assert result == "Web Search Counterargument"
    assert agent.gatekeeper.generate_response.call_count == 3


# --- ContextEngineeringMixin Tests ---

def test_update_memory_valid_json():
    agent = DummyAgent()
    agent.gatekeeper.generate_response.return_value = '{"my_arguments": ["Arg 1"], "opponent_arguments": [], "verified_facts": [], "invalidated_claims": []}'
    empty_memory = {}
    new_memory = agent.update_memory(empty_memory, "I claim AI is good.", "Pro")
    assert type(new_memory) is dict
    assert new_memory["my_arguments"][0] == "Arg 1"

def test_update_memory_fallback_on_bad_json():
    agent = DummyAgent()
    old_memory = {"my_arguments": ["Safe Memory"]}
    agent.gatekeeper.generate_response.return_value = "Sorry, I can't do that."
    new_memory = agent.update_memory(old_memory, "New turn", "Pro")
    assert new_memory == old_memory

def test_update_memory_fallback_on_missing_keys():
    """Hits the branch where JSON is valid, but missing the required schema keys."""
    agent = DummyAgent()
    old_memory = {"my_arguments": ["Safe Memory"]}
    # Valid JSON, but wrong schema
    agent.gatekeeper.generate_response.return_value = '{"wrong_key": "Oops"}'
    new_memory = agent.update_memory(old_memory, "New turn", "Pro")
    assert new_memory == old_memory