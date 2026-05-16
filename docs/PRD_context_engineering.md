# PRD: Context Window Engineering (Write/Select Strategy)

## 1. Overview & Problem Statement
In a 10-round multi-agent debate, passing the full conversation history to the LLM on every turn results in exponential token growth. This leads to high API costs, increased latency, and a degraded "Context Window," causing the model to forget earlier instructions (the "lost in the middle" phenomenon).

## 2. Proposed Mechanism: The "Write/Select" Summarization Mixin
To solve context explosion, this system implements the "Write/Select" context engineering strategy, encapsulated within the `ContextEngineeringMixin`.

### 2.1 How it Works
Instead of appending every new argument to a monolithic history array, the Mixin actively manages the context payload:
1. **The Active Window:** The agent is provided with the exact, verbatim text of the Judge's prompt and the opponent's *immediately preceding* argument.
2. **The Summarized Archive (Write):** All arguments older than $N-1$ are passed to a lightweight background LLM call. This call compresses the historical arguments into strict, high-density bullet points representing the core claims.
3. **The Re-injection (Select):** When generating the next prompt, the Mixin injects the compressed bullet points alongside the Active Window. 

## 3. Architecture & Constraints
* **Location:** `src/services/agent_mixins.py` -> `ContextEngineeringMixin`
* **Trigger:** Invoked automatically by the `BaseAgent` before calling the API Gatekeeper.
* **Fallback:** If the summarization API call fails, the system defaults to truncating the oldest messages to protect the Gatekeeper's token limits.

## 4. Success Criteria
* **Flat Token Curve:** The `prompt_token_count` across the 10 rounds must scale linearly or remain relatively constant, rather than growing exponentially.
* **Contextual Integrity:** The agents must still be able to reference historical arguments from Round 1 during Round 10, proving the compression did not destroy core debate facts.