"""
File: agents.py
Description: Core OOP Agent classes enforcing strict JSON IPC protocol.
"""

import json
from src.services.gatekeeper import ApiGatekeeper
from src.shared.config_loader import ConfigLoader
from src.services.agent_mixins import AdvancedReasoningMixin, ContextEngineeringMixin

class BaseAgent:
    """Base agent handling Gatekeeper initialization and JSON prompt execution."""

    def __init__(self, role_key: str):
        self.gatekeeper = ApiGatekeeper()
        self.role_key = role_key

        prompts = ConfigLoader.load_json("config/instructions/agent_prompts.json")
        if role_key not in prompts:
            raise ValueError(f"Role '{role_key}' missing from agent_prompts.json")

        self.instructions = prompts[role_key]["system_instruction"]
        self.guidelines = prompts[role_key]["response_guidelines"]

    def generate_response(self, topic: str, opponent_argument: str, memory_state: dict, rejection_notice: str = "") -> dict:
        """Calls the LLM and guarantees a JSON dictionary return."""

        # --- EXPLICIT JUDGE INSTRUCTIONS (HW REQUIREMENT) ---
        prompt = f"DEBATE TOPIC: {topic}\n\n"
        prompt += "JUDGE'S STRICT RULES OF PLAY:\n"
        prompt += "1. You must use respectful, parliamentary language.\n"
        prompt += f"2. You must strictly defend your assigned side ({self.role_key}).\n"
        prompt += "3. You must explicitly address and counter the opponent's previous claims.\n\n"

        prompt += f"Your Current Strategic Memory State: {json.dumps(memory_state)}\n\n"

        if opponent_argument:
            prompt += f"Opponent's Last Argument:\n'{opponent_argument}'\n\n"

        if rejection_notice:
            prompt += f"URGENT JUDGE REJECTION NOTICE:\n{rejection_notice}\n\n"

        prompt += (
            "Respond EXACTLY in this JSON format. No markdown blocks, no plain text outside JSON:\n"
            '{"thought_process": "...", "argument_summary": "...", "full_argument": "...", "addressed_opponent_points": ["..."], "sources_used": ["..."]}'
        )

        sys_instruct = f"{self.instructions}\n{self.guidelines}"

        response_text = self.gatekeeper.generate_response(
            agent_role=self.role_key,
            model_name="gemini-2.5-flash",
            prompt=prompt,
            system_instruction=sys_instruct,
            enable_search=False
        )

        try:
            clean_json = response_text.replace('```json', '').replace('```', '').strip()
            return json.loads(clean_json)
        except json.JSONDecodeError:
            return {
                "thought_process": "Error parsing LLM response.",
                "argument_summary": "JSON Structure Failure",
                "full_argument": "System failure: Agent generated invalid JSON. Turn forfeited.",
                "addressed_opponent_points": [],
                "sources_used": []
            }

class ProAgent(BaseAgent, AdvancedReasoningMixin, ContextEngineeringMixin):
    def __init__(self):
        super().__init__("pro_agent")

class ConAgent(BaseAgent, AdvancedReasoningMixin, ContextEngineeringMixin):
    def __init__(self):
        super().__init__("con_agent")