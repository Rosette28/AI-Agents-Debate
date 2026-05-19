"""
File: agents.py
Description:
Agent architecture for debate system.
"""

import json


class BaseAgent:
    """
    Base debate agent.
    """

    def __init__(self, name):
        """
        Initialize agent.

        Args:
            name (str): Agent name.
        """

        self.name = name

    def generate_response(self, argument):
        """
        Generate JSON response.

        Args:
            argument (str): Debate argument.

        Returns:
            dict
        """

        response = {
            "agent": self.name,
            "argument": argument
        }

        return json.dumps(response)