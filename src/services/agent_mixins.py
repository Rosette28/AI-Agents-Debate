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
    
class ContextEngineeringMixin:
    """
    Provides context summarization capability.
    """

    def summarize_context(self, text):
        """
        Summarize long context.

        Args:
            text (str): Input context.

        Returns:
            str
        """

        return text[:100]