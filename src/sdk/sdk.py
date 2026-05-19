"""
File: sdk.py
Description: Public API Facade providing the sole entry point for the presentation layer.
"""

# Placeholder import for the orchestrator we will build in Phase 5
# We use a lazy or local import inside methods if the file doesn't exist yet,
# but since we mock it in tests, we can structure the class properties cleanly.
class DebateSDK:
    """
    Unified interface managing underlying AI subcomponents.
    """

    def __init__(self):
        self.topic = None
        self._orchestrator = None

    def configure_debate(self, topic: str):
        """
        Public endpoint to set the current debate target.
        """
        if not topic or not topic.strip():
            raise ValueError("Debate topic cannot be empty.")
        self.topic = topic.strip()

    def run_debate(self):
        """
        Public endpoint to launch the 3-agent orchestration processes.
        """
        if not self.topic:
            raise ValueError("System Error: Configuration missing. Please set a topic first.")

        # Modern import pattern to bypass circular or missing dependencies during Phase 3
        from src.services.orchestrator import DebateOrchestrator

        self._orchestrator = DebateOrchestrator()
        self._orchestrator.initialize_debate(self.topic)
        self._orchestrator.run_debate_loop()