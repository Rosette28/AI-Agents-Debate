# AI Debate Arena

AI Debate Arena is a multi-agent debate system built using Python and Gemini API.

The system simulates structured debates between AI agents while a Judge agent evaluates persuasion quality and determines a winner.

---

# Features

- Multi-agent debate architecture
- JSON-based communication
- Interactive CLI menu
- Watchdog timeout recovery
- Rotating structured logs
- Context engineering
- Token economics analysis
- Unit testing with pytest
- Ruff linting support

---

# System Architecture

The project is built around:

- BaseAgent
- ProAgent
- ConAgent
- SearchMixin
- ContextEngineeringMixin
- DebateSDK
- Orchestrator
- Gatekeeper

---

# Interactive CLI

Run the system:

```bash
uv run python main.py