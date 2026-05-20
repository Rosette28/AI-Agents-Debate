from src.services.agent_mixins import (
    SearchMixin,
    ContextEngineeringMixin
)


class DummyAgent(
    SearchMixin,
    ContextEngineeringMixin
):
    pass


def test_search_web():
    """
    Test search mixin.
    """

    agent = DummyAgent()

    result = agent.search_web("AI")

    assert "AI" in result


def test_summarize_context():
    """
    Test context summarization.
    """

    agent = DummyAgent()

    text = "A" * 200

    result = agent.summarize_context(text)

    assert len(result) == 100