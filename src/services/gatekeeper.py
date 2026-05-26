"""
File: gatekeeper.py
Description: Centralized API wrapper handling timeouts, rate limits, and token economics.
"""

import os
import json
import time
import warnings
from datetime import datetime
import google.generativeai as genai
from src.shared.config_loader import ConfigLoader

# Suppress the Google Generative AI package deprecation warning
warnings.filterwarnings("ignore", category=FutureWarning, module="google.generativeai")


class ApiGatekeeper:
    """Tollbooth for all external LLM API calls."""

    def __init__(self):
        self.api_key = os.environ.get("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("CRITICAL: GEMINI_API_KEY environment variable not set.")
        
        genai.configure(api_key=self.api_key)
        self.rate_limits = ConfigLoader.load_json("config/rate_limits.json")
        self.rpm_limit = self.rate_limits.get("requests_per_minute", 15)
        self.timeout = self.rate_limits.get("timeout_seconds", 15)
        self.request_timestamps = []
        self.log_path = "data/results/token_logs.json"

    def _enforce_fifo_queue(self):
        """Asynchronous rate limiter to prevent 429 API crashes."""
        now = time.time()
        self.request_timestamps = [ts for ts in self.request_timestamps if now - ts < 60]
        if len(self.request_timestamps) >= self.rpm_limit:
            sleep_time = 60 - (now - self.request_timestamps[0])
            if sleep_time > 0:
                time.sleep(sleep_time)
        self.request_timestamps.append(time.time())

    def _log_token_economics(self, agent_role: str, usage_metadata):
        """Extract and save token costs."""
        if not usage_metadata:
            return
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "agent_role": agent_role,
            "prompt_tokens": getattr(usage_metadata, "prompt_token_count", 0),
            "completion_tokens": getattr(usage_metadata, "candidates_token_count", 0)
        }
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

    def generate_response(self, agent_role: str, model_name: str, prompt: str, 
                          system_instruction: str = None, enable_search: bool = False) -> str:
        """Execute API call with strict timeouts, rate limiting, and optional web search."""
        self._enforce_fifo_queue()
        
        # Enable Live Google Search Grounding if requested by the Mixin!
        tools = "google_search" if enable_search else None
        
        model = genai.GenerativeModel(
            model_name=model_name,
            system_instruction=system_instruction,
            tools=tools
        )
        response = model.generate_content(prompt, request_options={"timeout": self.timeout})
        self._log_token_economics(agent_role, response.usage_metadata)
        return response.text