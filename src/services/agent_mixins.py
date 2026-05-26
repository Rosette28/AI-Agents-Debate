import json

class AdvancedReasoningMixin:
    """Provides complex, multi-step cognitive workflows for agents."""
    
    def fact_check(self, claim: str) -> str:
        """1. Instantly searches the web for a specific fact to check it."""
        if not hasattr(self, 'gatekeeper'):
            raise AttributeError("Agent needs a gatekeeper.")
            
        prompt = (
            f"Search the web to verify this claim: '{claim}'.\n"
            "MANDATORY: Start your response with exactly [TRUE], [FALSE], or [OPINION].\n"
            "Provide a 2-sentence explanation and include the URL sources you found."
        )
        return self.gatekeeper.generate_response(
            agent_role="Subagent_FactChecker", 
            model_name="gemini-2.0-flash", 
            prompt=prompt, 
            enable_search=True
        )

    def look_for_arguments(self, topic: str, old_args: list) -> str:
        """2. Generates new arguments, filters duplicates, then searches web to validate."""
        # Step A: Brainstorm (No Search)
        draft_prompt = (
            f"Topic: {topic}.\nPreviously used arguments: {old_args}\n"
            "Brainstorm 2 brand new arguments that are completely different from the old ones. "
            "Just list them."
        )
        drafts = self.gatekeeper.generate_response(
            "Subagent_Brainstormer", "gemini-2.0-flash", draft_prompt, enable_search=False
        )

        # Step B: Validate and Source (With Search)
        validation_prompt = (
            f"Search the web to find real-world evidence for these proposed arguments: {drafts}.\n"
            "If an argument cannot be proven, discard it. Return only the valid arguments "
            "along with their supporting URL sources."
        )
        return self.gatekeeper.generate_response(
            "Subagent_Validator", "gemini-2.0-flash", validation_prompt, enable_search=True
        )

    def find_counterarguments(self, target_arg: str, old_args: list) -> str:
        """3. Fact-checks first. If true, checks old memory. If not found, searches web for counter."""
        # Step A: Check facts
        fact_result = self.fact_check(target_arg)
        if "[FALSE]" in fact_result or "[OPINION]" in fact_result:
            return f"Strategic Counter: The opponent's premise is flawed. {fact_result}"

        # Step B: Look in old arguments (No Search)
        memory_prompt = (
            f"Target to counter: '{target_arg}'.\nOur previous arguments: {old_args}.\n"
            "Can any of our previous arguments be used as a direct counter? "
            "If YES, start response with [FOUND] and explain how. If NO, reply EXACTLY with [NOT_FOUND]."
        )
        memory_check = self.gatekeeper.generate_response(
            "Subagent_Memory", "gemini-2.0-flash", memory_prompt, enable_search=False
        )
        
        if "[FOUND]" in memory_check:
            return memory_check

        # Step C: Search Web for new counter (With Search)
        search_prompt = (
            f"Search the web to find a strong, factual counterargument against this claim: '{target_arg}'.\n"
            "Provide the counterargument and include the URL sources."
        )
        return self.gatekeeper.generate_response(
            "Subagent_CounterSearch", "gemini-2.0-flash", search_prompt, enable_search=True
        )


class ContextEngineeringMixin:
    """Provides Incremental Rolling JSON State memory compression."""
    
    def update_memory(self, current_memory: dict, new_turn: str, my_role: str) -> dict:
        """
        Updates the agent's internal strategic state using old_memory + new_turn.
        Returns a dictionary enforcing the strict memory schema.
        """
        if not hasattr(self, 'gatekeeper'):
            raise AttributeError("Agent needs a gatekeeper.")
            
        # Default empty schema if this is Round 1
        if not current_memory:
            current_memory = {
                "my_arguments": [],
                "opponent_arguments": [],
                "verified_facts": [],
                "invalidated_claims": []
            }
            
        prompt = (
            f"You are the memory manager Subagent for the {my_role}.\n"
            f"Current Memory State: {json.dumps(current_memory)}\n"
            f"Newest Debate Turn: '{new_turn}'\n\n"
            "Update the memory state based on this new turn. "
            "Respond ONLY with a valid JSON object using exactly these keys: "
            "['my_arguments', 'opponent_arguments', 'verified_facts', 'invalidated_claims']. "
            "Do not use markdown code blocks."
        )
        
        response_text = self.gatekeeper.generate_response(
            "Subagent_MemoryManager", "gemini-2.0-flash", prompt, enable_search=False
        )
        
        # Safely parse the LLM output back into a Python dictionary
        try:
            clean_json = response_text.replace('```json', '').replace('```', '').strip()
            new_memory = json.loads(clean_json)
            # Ensure the required keys exist, otherwise fall back
            if "my_arguments" in new_memory:
                return new_memory
            return current_memory
        except json.JSONDecodeError:
            # Watchdog pattern: If the LLM formats it wrong, keep the old safe memory
            return current_memory