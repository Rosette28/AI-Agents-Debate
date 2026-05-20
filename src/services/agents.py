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
        
        # Load instructions dynamically from Phase 2 configuration
        prompts = ConfigLoader.load_json("config/instructions/agent_prompts.json")
        if role_key not in prompts:
            raise ValueError(f"Role '{role_key}' missing from agent_prompts.json")
            
        self.instructions = prompts[role_key]["system_instruction"]
        self.guidelines = prompts[role_key]["response_guidelines"]
        
    def generate_response(self, topic: str, opponent_argument: str, memory_state: dict, rejection_notice: str = "") -> dict:
        """Calls the LLM and guarantees a JSON dictionary return (Inter-Process Communication)."""
        
        # Construct the context payload
        prompt = f"Debate Topic: {topic}\n"
        prompt += f"Your Current Strategic Memory State: {json.dumps(memory_state)}\n\n"
        
        if opponent_argument:
            prompt += f"Opponent's Last Argument:\n'{opponent_argument}'\n\n"
            
        if rejection_notice:
            # If the Judge rejected the last turn, append the correction payload here
            prompt += f"URGENT JUDGE REJECTION NOTICE:\n{rejection_notice}\n\n"
            
        # Strict schema enforcement for the API
        prompt += (
            "Respond EXACTLY in this JSON format. No markdown blocks, no plain text outside JSON:\n"
            '{"thought_process": "...", "argument_summary": "...", "full_argument": "...", "addressed_opponent_points": ["..."], "sources_used": ["..."]}'
        )
        
        sys_instruct = f"{self.instructions}\n{self.guidelines}"
        
        response_text = self.gatekeeper.generate_response(
            agent_role=self.role_key,
            model_name="gemini-1.5-flash",
            prompt=prompt,
            system_instruction=sys_instruct,
            enable_search=False  # Main generation doesn't search directly, the Subagents do that before this is called
        )
        
        # JSON Watchdog parsing
        try:
            clean_json = response_text.replace('```json', '').replace('```', '').strip()
            return json.loads(clean_json)
        except json.JSONDecodeError:
            # Graceful degradation if the LLM hallucinates formatting
            return {
                "thought_process": "Error parsing LLM response.",
                "argument_summary": "JSON Structure Failure",
                "full_argument": "System failure: Agent generated invalid JSON. Turn forfeited.",
                "addressed_opponent_points": [],
                "sources_used": []
            }

class ProAgent(BaseAgent, AdvancedReasoningMixin, ContextEngineeringMixin):
    """The affirmative debater thread."""
    def __init__(self):
        super().__init__("pro_agent")

class ConAgent(BaseAgent, AdvancedReasoningMixin, ContextEngineeringMixin):
    """The negative debater thread."""
    def __init__(self):
        super().__init__("con_agent")