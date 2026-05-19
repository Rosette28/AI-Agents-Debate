"""
File: gatekeeper.py
Description: Centralized API wrapper handling timeouts, rate limits, and token economics.
"""

import os
import json
import time
from datetime import datetime
import google.generativeai as genai
from src.shared.config_loader import ConfigLoader


class ApiGatekeeper:
    """
    Tollbooth for all external LLM API calls.
    """

    def __init__(self):
        # 1. Secure API Key Loading
        self.api_key = os.environ.get("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("CRITICAL: GEMINI_API_KEY environment variable not set.")
        
        genai.configure(api_key=self.api_key)

        # 2. Load constraints from Phase 2 configs
        self.rate_limits = ConfigLoader.load_json("config/rate_limits.json")
        self.rpm_limit = self.rate_limits.get("requests_per_minute", 15)
        self.timeout = self.rate_limits.get("timeout_seconds", 15)

        # 3. Initialize FIFO Queue variables and Token Logger path
        self.request_timestamps = []
        self.log_path = "data/results/token_logs.json"

        # Ensure the JSON log array exists
        if not os.path.exists(self.log_path):
            with open(self.log_path, "w", encoding="utf-8") as f:
                json.dump([], f)

    def _enforce_fifo_queue(self):
        """Asynchronous rate limiter to prevent 429 API crashes."""
        now = time.time()
        
        # Clear timestamps older than 60 seconds
        self.request_timestamps = [ts for ts in self.request_timestamps if now - ts < 60]

        # If we hit the limit, freeze the thread until a slot opens up
        if len(self.request_timestamps) >= self.rpm_limit:
            sleep_time = 60 - (now - self.request_timestamps[0])
            if sleep_time > 0:
                time.sleep(sleep_time)

        # Register the new request
        self.request_timestamps.append(time.time())

    def _log_token_economics(self, agent_role: str, usage_metadata):
        """Extract and save token costs for the Jupyter Notebook analysis."""
        if not usage_metadata:
            return

        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "agent_role": agent_role,
            "prompt_tokens": getattr(usage_metadata, "prompt_token_count", 0),
            "completion_tokens": getattr(usage_metadata, "candidates_token_count", 0)
        }

        # FIX: Ensure the file always exists before opening in "r+" mode
        if not os.path.exists(self.log_path):
            with open(self.log_path, "w", encoding="utf-8") as f:
                json.dump([], f)

        with open(self.log_path, "r+", encoding="utf-8") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = []
            
            data.append(log_entry)
            f.seek(0)
            json.dump(data, f, indent=4)
            f.truncate()

    def generate_response(self, agent_role: str, model_name: str, prompt: str, system_instruction: str = None) -> str:
        """
        Execute API call with strict timeouts, rate limiting, and cost tracking.
        """
        self._enforce_fifo_queue()

        model = genai.GenerativeModel(
            model_name=model_name,
            system_instruction=system_instruction
        )

        # Execute with the strict 15-second Watchdog timeout constraint
        response = model.generate_content(
            prompt,
            request_options={"timeout": self.timeout}
        )

        self._log_token_economics(agent_role, response.usage_metadata)

        return response.text