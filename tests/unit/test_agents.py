from src.services.agents import (
    ProAgent,
    ConAgent
)


def test_pro_agent():
    """
    Test ProAgent.
    """

    agent = ProAgent("PRO")

    response = agent.generate_response(
        "AI is beneficial"
    )

    assert response["agent"] == "PRO"


def test_con_agent():
    """
    Test ConAgent.
    """

    agent = ConAgent("CON")

    response = agent.generate_response(
        "AI is dangerous"
    )

    assert response["agent"] == "CON"