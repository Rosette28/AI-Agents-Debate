"""
Tests for Advanced Reasoning Mixins (Skills).
"""

from unittest.mock import MagicMock
from src.services.agent_mixins import AdvancedReasoningMixin


class DummyAgent(AdvancedReasoningMixin):
    """A dummy agent to test mixin inheritance."""
    def __init__(self):
        self.gatekeeper = MagicMock()


def test_fact_check_uses_live_search():
    """Test that fact checking triggers the gatekeeper with enable_search=True."""
    agent = DummyAgent()
    agent.gatekeeper.generate_response.return_value = "[FALSE] The moon is rock. Source: nasa.gov"
    
    result = agent.fact_check("The moon is made of cheese")
    assert "[FALSE]" in result
    
    # Assert enable_search=True was passed to the gatekeeper
    _, kwargs = agent.gatekeeper.generate_response.call_args
    assert kwargs.get("enable_search") is True


def test_find_new_arguments_two_step_process():
    """Test that it generates drafts without search, then validates WITH search."""
    agent = DummyAgent()
    # 1st call (drafts), 2nd call (validation)
    agent.gatekeeper.generate_response.side_effect = [
        "Draft Argument 1", 
        "Valid: Draft 1. Source: URL"
    ]
    
    result = agent.look_for_arguments("AI", ["Old Arg 1"])
    assert "Valid:" in result
    assert agent.gatekeeper.generate_response.call_count == 2


def test_find_counterargument_fact_check_fails():
    """Test that if the target argument is a FALSE fact, it stops and returns the correction."""
    agent = DummyAgent()
    # The fact checker instantly returns [FALSE]
    agent.gatekeeper.generate_response.return_value = "[FALSE] That is incorrect."
    
    result = agent.find_counterarguments("Sky is green", [])
    assert "[FALSE]" in result
    # It should only call the API once (for the fact check), skipping the rest of the workflow
    assert agent.gatekeeper.generate_response.call_count == 1