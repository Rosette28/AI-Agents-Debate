# Professional AI Debate Arena: Multi-Agent Orchestration System

## Project Overview

This project implements a highly structured, multi-agent AI debate simulation utilizing the Google Gemini API. The objective is to orchestrate a fully autonomous 10-round debate between two distinct AI personas (Pro and Con) on a user-defined topic, culminating in a definitive, mathematically graded verdict by an impartial AI Judge.

Unlike simple chatbot interfaces, this system relies on strict Inter-Process Communication (IPC), Object-Oriented Mixins, and autonomous error-recovery mechanisms to maintain continuous agentic loops without human intervention. This repository serves as a complete demonstration of advanced prompt engineering, O(1) context memory management, and Plan-and-Solve cognitive workflows.

---

# 1. Core Features

The system is built with enterprise-grade resiliency and architectural patterns, featuring:

- **Multi-agent debate architecture:** Orchestrates distinct AI personas (Pro, Con, and Judge) interacting autonomously within a structured, zero-sum environment.
- **JSON-based communication:** Enforces strict Inter-Process Communication (IPC) contracts. Agents never communicate via raw strings; all outputs are machine-readable dictionaries, allowing programmatic validation.
- **Interactive CLI menu:** Provides a decoupled, user-friendly terminal interface to configure topics, launch the simulation, and view the final evaluated verdicts.
- **Watchdog timeout recovery:** Automatically intercepts API timeouts, JSON formatting hallucinations, and word-count rule violations. It forces agent retries via structured rejection payloads to completely prevent Python system crashes.
- **Rotating structured logs:** Maintains a rolling history of system events (`app.log`) using Python's `RotatingFileHandler` with strict file size boundaries to prevent disk bloat.
- **Context engineering:** Implements an O(1) rolling state memory to compress debate history. It tracks claims and facts incrementally, eliminating token explosion and context degradation.
- **Token economics analysis:** Asynchronously tracks and logs prompt/completion token usage (`usage_metadata`) for every API call to a local dataset for financial cost monitoring.
- **Unit testing with pytest:** Ensures high reliability and strict Test-Driven Development (TDD) compliance across all core modules before business logic execution.
- **Ruff linting support:** Enforces blazing-fast PEP-8 code quality, formatting, and structural standards.

---

# 2. System Architecture Components

The project strictly follows Object-Oriented Programming (OOP) principles, ensuring zero code duplication and clear Separation of Concerns. The architecture is built around the following core components:

- **BaseAgent:** The foundational parent class. It handles Gatekeeper initialization, payload construction, and enforces the strict JSON response schema required by the API.
- **ProAgent:** Inherits from `BaseAgent`. Acts as the affirmative debater thread, dynamically loading its aggressive, pro-topic persona from configuration files.
- **ConAgent:** Inherits from `BaseAgent`. Acts as the negative debater thread, utilizing critical analysis to systematically dismantle the affirmative claims.
- **SearchMixin (Advanced Reasoning):** Injects live Google Search Grounding and multi-step Plan-and-Solve workflows (Fact-Checking, Drafting, Validating) into the agents without polluting the base class.
- **ContextEngineeringMixin:** Provides the incremental JSON memory compression logic. It safely parses and updates the agent's internal strategic state (verified facts, opponent arguments) after every turn.
- **DebateSDK:** The facade pattern entry point. It cleanly isolates the complex orchestration business logic from the presentation layer (the CLI menu).
- **Orchestrator:** The central processing engine (`DebateOrchestrator`). It manages the 10-round turn rotations, acts as the Watchdog validator, and generates the final persuasion-graded verdict.
- **Gatekeeper:** The centralized API wrapper (`ApiGatekeeper`). It securely loads credentials, enforces FIFO (First-In, First-Out) rate limits, and manages 15-second expiration timeouts.

---

# 3. Installation & Setup

To run this simulation locally, you must configure your environment to safely interact with the Gemini API without exposing secure credentials.

## 3.1 System Requirements

- **Operating System:** Windows 10/11, macOS, or Linux.
- **Python Version:** Python 3.12 or higher.
- **Package Manager:** `uv` (The extremely fast Python package manager).

## 3.2 Step-by-Step Installation

### 1. Clone the Repository

```bash
git clone https://github.com/YourUsername/AI-Agents-Debate.git
cd AI-Agents-Debate
```

### 2. Synchronize Dependencies

Using `uv`, sync the project dependencies to automatically build your virtual environment:

```bash
uv sync
```

### 3. Environment Variable Setup

For strict security compliance, API keys must never be hardcoded. Export your Gemini API key.

#### On Windows (PowerShell)

```powershell
$env:GEMINI_API_KEY="your_api_key_here"
```

#### On macOS/Linux (Bash/Zsh)

```bash
export GEMINI_API_KEY="your_api_key_here"
```

---

# 4. Interactive CLI & Usage

The system is entirely decoupled from the presentation layer. You initiate the debate via the unified SDK entry point using a standard Interactive Command Line Interface (CLI).

## 4.1 Running the System

From the root directory, execute the following command:

```bash
uv run python main.py
```

## 4.2 Typical Execution Workflow

When the interactive menu boots, you will follow a standard 3-step workflow:

1. **Option 1: Set Debate Topic.**  
   You will be prompted to enter a contentious topic. The SDK saves this to state.

2. **Option 2: Run Debate.**  
   This hands control over to the `DebateOrchestrator`. You will watch the terminal as the Pro and Con agents iteratively generate their arguments. You will also see the Watchdog in action if it catches an agent violating a rule and forces a retry.

3. **Option 3: View Final Verdict.**  
   After the loop concludes, selecting this option prints the Judge's final markdown evaluation to the console, detailing argument strengths, numerical scores, and the absolute winner.

---

# 5. Configuration Guide

The system is heavily parameterized. All configuration is managed via files in the `config/` directory.

- **`config/setup.json`**  
  Enforces system metadata, max round limits, and logging boundaries.

- **`config/rate_limits.json`**  
  Controls the `ApiGatekeeper` queue (`requests_per_minute`) and timeouts.

- **`config/instructions/agent_prompts.json`**  
  Holds the distinct personas and response guidelines for the agents.

- **`config/instructions/judge_rules.txt`**  
  The plaintext rulebook injected into the Orchestrator, containing absolute mandates (e.g., prohibition of ties).

---

# 6. Examples & Visualizations

## 6.1 Live Debate Execution

During execution, the system logs the thought processes and Watchdog interactions to the terminal. The Watchdog successfully intercepts rule violations (such as word-count limits) and forces immediate retries, ensuring the Python loop never crashes.

## 6.2 The Final Judge's Decision (Output Example)

At the conclusion of Round 10, the Orchestrator passes the entire validated transcript to a higher-reasoning model (`gemini-1.5-pro`) to evaluate persuasion. The Judge generates a strict markdown verdict, actively deducting points for Watchdog disqualifications.

---

# 7. Theoretical Background: The Context Explosion Problem

In a standard LLM loop, appending the full conversation history to the prompt every turn results in exponential token growth, leading to API rate limit crashes.

To solve this, our system implements an **O(1) Incremental JSON Rolling State**. Instead of re-reading the entire transcript, the `ContextEngineeringMixin` updates a lean, strategic JSON object at the end of each turn.

It tracks:

- `my_arguments`
- `opponent_arguments`
- `verified_facts`
- `invalidated_claims`

This keeps the API token curve completely flat.

---

# 8. Contribution & Code Standards

If you are contributing to this repository, you must adhere to strict architectural standards:

1. **Strict OOP & Mixins**  
   No massive monolithic classes. Capabilities must be modular Mixins.

2. **The 150-Line Rule**  
   No single Python file may exceed 150 lines of code.

3. **Test-Driven Development (TDD)**  
   Every new feature must be accompanied by a `pytest` unit test *before* implementation.

4. **Linting**  
   All code must pass `ruff` formatting perfectly.

   Run:

   ```bash
   uv run ruff check .
   ```

5. **No Presentation Logic in Business Tier**  
   `print()` statements belong exclusively in `main.py` or `sdk.py`.

---

# 9. License & Credits

## License

Released under the MIT License.

## Third-Party Acknowledgements

- **Google Generative AI SDK**  
  Used to interface with Gemini 1.5 Flash and Pro, including Live Search Grounding capabilities.

- **Pytest & Ruff**  
  Utilized for TDD compliance and PEP-8 style enforcement.

- **Astral (`uv`)**  
  Leveraged for high-speed dependency resolution.