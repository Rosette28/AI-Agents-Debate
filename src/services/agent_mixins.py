"""
File: agent_mixins.py
Description:
Mixin classes for debate agents.
"""


class SearchMixin:
    """
    Provides web search capability.
    """

    def search_web(self, query):
        """
        Simulate web search.

        Args:
            query (str): Search query.

        Returns:
            str
        """

        return "Search results for: " + query