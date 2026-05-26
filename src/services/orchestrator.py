"""
File: orchestrator.py
Description: Manages the 10-round debate loop, Watchdog recovery, and final persuasion grading.
"""

import os
import json
import logging
from src.services.agents import ProAgent, ConAgent
from src.services.gatekeeper import ApiGatekeeper

os.makedirs("data/logs", exist_ok=True)
logging.basicConfig(
    filename="data/logs/app.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

class DebateOrchestrator:
    def __init__(self):
        self.gatekeeper = ApiGatekeeper()
        self.pro_agent = ProAgent()
        self.con_agent = ConAgent()
        self.topic = ""
        self.history = []
        self.total_rounds = 10

        try:
            with open("config/instructions/judge_rules.txt", "r", encoding="utf-8") as f:
                self.judge_instructions = f.read()
        except FileNotFoundError:
            self.judge_instructions = "You are an elite, impartial debate judge. No ties allowed."

    def initialize_debate(self, topic: str):
        self.topic = topic
        logging.info(f"Debate initialized with topic: {self.topic}")

    def _validate_argument(self, response: dict) -> tuple[bool, str]:
        if not isinstance(response, dict) or "full_argument" not in response:
            return False, "Response is not a valid JSON dictionary."

        full_arg = response["full_argument"]

        if len(full_arg.split()) > 100:
            return False, "Your argument contained too many words, exceeding the maximum allowed limit of 100 words."

        if "addressed_opponent_points" not in response or not response["addressed_opponent_points"]:
            return False, "You failed to explicitly address the opponent's previous points."

        return True, ""

    def _watchdog_retry(self, agent, opponent_arg: str, memory_state: dict, error_msg: str) -> dict:
        logging.warning(f"Watchdog triggered for {agent.role_key}: {error_msg}")

        rejection_notice = json.dumps({
            "status": "REJECTED",
            "error_type": "VALIDATION_VIOLATION",
            "violation_details": error_msg,
            "correction_instruction": "Regenerate your argument immediately. Ensure it is strictly formatted and complies with constraints."
        })

        try:
            new_response = agent.generate_response(self.topic, opponent_arg, memory_state, rejection_notice)
            is_valid, _ = self._validate_argument(new_response)
            if is_valid:
                return new_response
            return {"full_argument": "[AGENT DISQUALIFIED ON RETRY DUE TO REPEATED VIOLATION]"}
        except Exception as e:
            logging.error(f"Watchdog fatal retry error: {str(e)}")
            return {"full_argument": "[AGENT SYSTEM CRASH]"}

    def run_debate_loop(self):
        print(f"\n[JUDGE] Starting {self.total_rounds}-round debate on: '{self.topic}'\n")

        pro_memory = {}
        con_memory = {}
        last_con_arg = ""

        for round_num in range(1, self.total_rounds + 1):
            print(f"--- Round {round_num} ---")

            print("Processing Pro Agent turn...")
            pro_resp = self.pro_agent.generate_response(self.topic, last_con_arg, pro_memory)
            is_valid, error = self._validate_argument(pro_resp)
            if not is_valid:
                pro_resp = self._watchdog_retry(self.pro_agent, last_con_arg, pro_memory, error)

            last_pro_arg = pro_resp.get("full_argument", "")
            print(f"\n[PRO AGENT]:\n{last_pro_arg}\n")
            self.history.append({"role": "PRO", "argument": last_pro_arg})

            if hasattr(self.pro_agent, "update_memory"):
                pro_memory = self.pro_agent.update_memory(pro_memory, last_pro_arg, "ProAgent")

            print("Processing Con Agent turn...")
            con_resp = self.con_agent.generate_response(self.topic, last_pro_arg, con_memory)
            is_valid, error = self._validate_argument(con_resp)
            if not is_valid:
                con_resp = self._watchdog_retry(self.con_agent, last_pro_arg, con_memory, error)

            last_con_arg = con_resp.get("full_argument", "")
            print(f"\n[CON AGENT]:\n{last_con_arg}\n")
            self.history.append({"role": "CON", "argument": last_con_arg})

            if hasattr(self.con_agent, "update_memory"):
                con_memory = self.con_agent.update_memory(con_memory, last_con_arg, "ConAgent")

        self.conclude_debate()

    def conclude_debate(self):
        print("\n[JUDGE] Debate concluded. Analyzing transcript and generating verdict...")

        transcript = "\n\n".join([f"{entry['role']} AGENT:\n{entry['argument']}" for entry in self.history])

        prompt = (
            f"You are the master judge evaluating the following debate on: '{self.topic}'.\n\n"
            f"FULL TRANSCRIPT:\n{transcript}\n\n"
            "Generate a deep, comprehensive final decision formatted in strict markdown containing exactly:\n"
            "1. **Debate Summary:** Summarize the core clash and overall conversation.\n"
            "2. **Argument Strengths:** Present ALL the main arguments made by BOTH sides. Evaluate exactly how strong each argument is.\n"
            "3. **Numerical Grades:** Give a final score out of 100 for both PRO and CON.\n"
            "4. **Final Winner:** Clearly decide who won based on persuasion. TIES ARE STRICTLY FORBIDDEN."
        )

        verdict = self.gatekeeper.generate_response(
            agent_role="JudgeOrchestrator",
            model_name="gemini-2.0-flash",
            prompt=prompt,
            system_instruction=self.judge_instructions,
            enable_search=False
        )

        os.makedirs("data/results", exist_ok=True)
        with open("data/results/final_decision.md", "w", encoding="utf-8") as f:
            f.write(f"# Debate Topic: {self.topic}\n\n")
            f.write(verdict)

        print("[JUDGE] Verdict generation complete. Results saved to 'data/results/final_decision.md'.")