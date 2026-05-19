# Project Task Backlog: Multi-Agent Debate System (v1.00)

## Phase 1: Infrastructure, Planning & Architecture Verification
**Phase Objective:** Initialize version tracking control, build the directory architecture, and secure baseline approval for technical frameworks before coding begins.

### Task 1.1: Environment Initialization & Directory Scaffolding
* **Priority:** High
* **Assignee:** Partner A
* **Definition of Done (DoD):** Repository initialized with `uv`, modular sub-folders (`src/sdk`, `src/services`, `src/shared`, `tests/unit`, `docs`, `config/instructions`, `data/logs`, `data/results`, `data/notebooks`, `assets`) generated, and global version tracked in `src/shared/version.py`.
* **Status:** [x]

### Task 1.2: General Product Requirements Formulation
* **Priority:** High
* **Assignee:** Partner A
* **Definition of Done (DoD):** `docs/PRD.md` drafted, detailing the 3-agent structure, dynamic topic initialization, 10-round interaction limits, and persuasion-based grading policies.
* **Status:** [x]

### Task 1.3: Specific Algorithmic & Mechanism PRD Drafting
* **Priority:** High
* **Assignee:** Partner A
* **Definition of Done (DoD):** Separate specialized PRD documents created inside the `docs/` folder: agent_architecture, context_engineering, and token_economics
* **Status:** [x]

### Task 1.4: System Blueprint Design & Modeling Completion
* **Priority:** High
* **Assignee:** Partner A
* **Definition of Done (DoD):** C4 Model Context/Container charts, operational deployment frameworks, JSON data interface schemas, and core ADR rationales compiled and rendering inside `docs/PLAN.md`.
* **Status:** [x]

---

## Phase 2: Configuration Tier & Logging Infrastructure
**Phase Objective:** Isolate configuration variables and implement a strict, rotating file logging subsystem following test-driven guidelines.

### Task 2.1: Populate Static Instruction Manifests & Rate Parameters
* **Priority:** High
* **Assignee:** Partner B
* **Definition of Done (DoD):** `config/setup.json` and `config/rate_limits.json` populated with version arrays (`"version": "1.00"`) and API query parameters; system prompts extracted to `config/instructions/agent_prompts.json`.
* **Status:** [x]

### Task 2.2: Implement TDD Configuration Loader Unit Tests
* **Priority:** High
* **Assignee:** Partner B
* **Definition of Done (DoD):** `tests/unit/test_config.py` written *before* implementation, asserting parameter integrity constraints, parsing exceptions, and system version checking validations.
* **Status:** [x]

### Task 2.3: Build Configuration Loading Subsystem
* **Priority:** High
* **Assignee:** Partner B
* **Definition of Done (DoD):** `src/shared/config_loader.py` completed under 150 lines, successfully passing all unit tests and enforcing metadata alignment constraints.
* **Status:** [x]

### Task 2.4: Implement Structured Rotating File Logger Subsystem
* **Priority:** High
* **Assignee:** Partner B
* **Definition of Done (DoD):** `src/shared/logger.py` written and verified using a `RotatingFileHandler` that dynamically loads file boundaries (`max_files=20`, `max_lines=500`) directly from configuration metadata.
* **Status:** [x]

---

## Phase 3: Gateway Tier, Security Guardrails & Unified SDK
**Phase Objective:** Set up a centralized API access controller to protect secrets and wrap the business tier under an entry point facade.

### Task 3.1: Write TDD Guardrails for API Access Control
* **Priority:** High
* **Assignee:** Partner A
* **Definition of Done (DoD):** `tests/unit/test_gatekeeper.py` written, defining unit tests that verify request routing behavior, rate limit interceptions, and handling of broken connection strings.
* **Status:** [ ]

### Task 3.2: Build Centralized API Gatekeeper with Token Economy Logging
* **Priority:** High
* **Assignee:** Partner A
* **Definition of Done (DoD):** `src/services/gatekeeper.py` built under 150 lines, consuming credentials strictly via `os.environ.get("GEMINI_API_KEY")`, and appending raw `usage_metadata` logs directly to `data/results/token_logs.json`.
* **Status:** [ ]

### Task 3.3: Implement API Rate Overflow Management and Expiry Limits
* **Priority:** High
* **Assignee:** Partner A
* **Definition of Done (DoD):** API call handling implements an internal FIFO pipeline that cues overflowing operations instead of crashing, alongside a strict 15-second response expiration ceiling
* **Status:** [ ]

### Task 3.4: Write TDD Specifications for the SDK Facade
* **Priority:** High
* **Assignee:** Partner A
* **Definition of Done (DoD):** `tests/unit/test_sdk.py` written, specifying input expectations for system instantiation, state updates, and programmatic result retrieval.
* **Status:** [ ]

### Task 3.5: Build the Unified System SDK Layer
* **Priority:** High
* **Assignee:** Partner A
* **Definition of Done (DoD):** `src/sdk/sdk.py` implemented as the single operational entry point for all underlying logic layers; direct business execution inside presentation scripts is completely locked out
* **Status:** [ ]

---

## Phase 4: OOP Mixins & Asymmetric Agent State Engines
**Phase Objective:** Write the core agent definitions using class inheritance patterns, incorporating search mechanics and memory management mixins.

### Task 4.1: Write TDD Specifications for Capabilities Mixins
* **Priority:** High
* **Assignee:** Partner B
* **Definition of Done (DoD):** `tests/unit/test_mixins.py` created, verifying clean execution of search modules, data filtering behaviors, and history summary calculations.
* **Status:** [ ]

### Task 4.2: Build Search and Verification Mixin Component
* **Priority:** High
* **Assignee:** Partner B
* **Definition of Done (DoD):** `SearchAndFactCheckMixin` added to `src/services/agent_mixins.py`, enabling model function calling to search the live web and verify claims.
* **Status:** [ ]

### Task 4.3: Build "Write/Select" Context Engineering Memory Mixin
* **Priority:** High
* **Assignee:** Partner B
* **Definition of Done (DoD):** `ContextEngineeringMixin` completed, implementing background LLM history compression routines to keep primary context window allocations low.
* **Status:** [ ]

### Task 4.4: Write TDD Contracts for Concrete Agent Definitions
* **Priority:** High
* **Assignee:** Partner B
* **Definition of Done (DoD):** `tests/unit/test_agents.py` written, asserting prompt assembly rules, role personas, and strict JSON output formats.
* **Status:** [ ]

### Task 4.5: Build BaseAgent and Inherited Pro/Con Subclasses
* **Priority:** High
* **Assignee:** Partner B
* **Definition of Done (DoD):** `BaseAgent`, `ProAgent`, and `ConAgent` objects fully written under the 150-line maximum length constraint, natively forcing and parsing structured JSON communications.
* **Status:** [ ]

### Task 4.6: Implement Complex Reasoning Subagent Spawners
* **Priority:** Medium
* **Assignee:** Partner B
* **Definition of Done (DoD):** `LogicalReasoningMixin` added, allowing active agents to spawn short-lived background Subagents for deep argumentation analysis before returning text
* **Status:** [ ]

---

## Phase 5: Dialogue Orchestration & Watchdog Recovery Loops
**Phase Objective:** Build the main mediation processing architecture to manage dialogue turns, validation routines, and system failures.

### Task 5.1: Write TDD Specifications for the Dialogue Orchestrator
* **Priority:** High
* **Assignee:** Partner A
* **Definition of Done (DoD):** `tests/unit/test_orchestrator.py` compiled, verifying turn rotation tracking, verification errors, and simulated connection recovery steps.
* **Status:** [ ]

### Task 5.2: Build Mediated Debate Loop Engine
* **Priority:** High
* **Assignee:** Partner A
* **Definition of Done (DoD):** `DebateOrchestrator` in `src/services/orchestrator.py` implemented to run exactly 10 round turns, routing all data payloads exclusively through the Judge process
* **Status:** [ ]

### Task 5.3: Build Programmatic Response Validators
* **Priority:** High
* **Assignee:** Partner A
* **Definition of Done (DoD):** Hardcoded validation checks for JSON payload structure, 100-word thresholds, and semantic engagement assertions added to the Judge loop
* **Status:** [ ]

### Task 5.4: Integrate Resiliency Watchdog Recovery Subsystem
* **Priority:** High
* **Assignee:** Partner A
* **Definition of Done (DoD):** Programmatic `try-except` try blocks implemented around agent executions; returns structured correction messages (`status: REJECTED`) to handle exceptions gracefully
* **Status:** [ ]

### Task 5.5: Build Graded Verdict Generation Logic
* **Priority:** High
* **Assignee:** Partner A
* **Definition of Done (DoD):** `conclude_debate()` method completed, enforcing an absolute winner constraint (0% tie rate) and exporting a detailed evaluation file to `data/results/final_decision.md`.
* **Status:** [ ]

---

## Phase 6: System Presentation, Empirical Analysis & Lab Report
**Phase Objective:** Package the engine behind an interactive CLI menu, assert code coverage targets, run cost notebooks, and write the user manual.

### Task 6.1: Build Interactive Keyboard Terminal Menu UI
* **Priority:** High
* **Assignee:** Partner B
* **Definition of Done (DoD):** `main.py` completed with a keyboard-driven loop (`while True`) providing options to configure parameters, run debates, and extract files exclusively via the SDK layer
* **Status:** [ ]

### Task 6.2: Execute Static Quality Analysis and Code Review Controls
* **Priority:** High
* **Assignee:** Partner B
* **Definition of Done (DoD):** `uv run ruff check .` executed with zero warnings; `uv run pytest --cov=src` confirming global test coverage exceeds the strict 85% requirement.
* **Status:** [ ]

### Task 6.3: Implement Financial Token Economics & Sensitivity Research
* **Priority:** High
* **Assignee:** Partner B
* **Definition of Done (DoD):** `data/notebooks/token_analysis.ipynb` compiled, displaying visualizations of input/output distributions, USD cost calculations, and OAT sensitivity curves comparing agent behavior at `temp=0.2` versus `temp=0.8`.
* **Status:** [ ]

### Task 6.4: Finalize Comprehensive Lab Manual (README.md)
* **Priority:** High
* **Assignee:** Partner B
* **Definition of Done (DoD):** Root `README.md` completed, incorporating an OOP class hierarchy diagram, CLI operational guides, financial metrics, and a transcript log of an entire debate session.
* **Status:** [ ]