# Product Requirements Document (PRD): Multi-Agent Debate System

## 1. Project Overview & Context
The Multi-Agent Debate System is an interactive, terminal-based AI application that orchestrates a highly structured, 10-round debate between two opposing AI agents (Pro and Con), mediated by a third AI agent acting as the Judge. The project demonstrates advanced LLM orchestration, Inter-Process Communication (IPC) via structured JSON, Context Window Engineering, and robust API failure recovery mechanisms.

## 2. Target Audience & Problem Statement
* **Target Audience:** people wishing to observe autonomous, logic-driven AI debates.
* **Problem Statement:** Standard LLM interactions rely on simple prompt-response loops that lack autonomy, struggle with context limits over long sessions, and fail unpredictably. This system solves these issues by introducing an orchestration layer (the Judge), a safety layer (the Watchdog and Gatekeeper), and a memory optimization layer (Write/Select Context Engineering).

## 3. Goals & Key Performance Indicators (KPIs)
* **Goal 1:** Achieve 100% autonomous execution of a 10-round debate without manual intervention.
* **Goal 2:** Enforce strict rule compliance (word counts, tone, JSON formatting) via Judge validation.
* **Goal 3:** Prevent context window explosion and track API costs efficiently.

**KPIs / Acceptance Criteria:**
* **Pass Rate:** 100% of inter-agent communication must be successfully parsed as JSON.
* **Resilience:** System must successfully catch and recover from simulated or actual API timeouts (15-second threshold).
* **Cost Efficiency:** Token economics must be actively logged for every API call.
* **Decisiveness:** 100% of final verdicts must declare a definitive winner (0% tie rate).

## 4. Functional Requirements

### 4.1 Interactive CLI & Dynamic Setup
* **REQ-F1:** The system must launch with an interactive terminal menu (Set Topic, Run Debate, View Verdict, Exit).
* **REQ-F2:** The debate topic must be dynamically provided by the user at runtime.

### 4.2 Agent Roles & Capabilities
* **REQ-F3 (The Judge Agent):** Acts as the central orchestrator. It does not argue; it validates responses, enforces the 100-word limit, and dictates the flow of turns.
* **REQ-F4 (Pro & Con Agents):** Must adopt their assigned personas, actively rebut their opponent's previous points, and utilize assigned skills (e.g., Internet Search).

### 4.3 The Debate Loop & Inter-Process Communication (IPC)
* **REQ-F5:** Agents must never communicate directly. Flow must be: Pro -> Judge -> Con -> Judge.
* **REQ-F6:** **Strict JSON Protocol:** All internal communications between agents and the orchestrator must be formulated and parsed as JSON payloads.

### 4.4 Final Verdict & Grading
* **REQ-F7:** At the conclusion of round 10, the Judge must evaluate the debate.
* **REQ-F8:** Grading must be based strictly on **persuasion and rhetoric**, not factual accuracy (bluffing is permitted if convincing).
* **REQ-F9:** The Judge must output a final markdown file (`data/results/final_decision.md`) containing a summary, argument strength analysis, numerical scores, and a definitive winner (ties are strictly forbidden).

## 5. Non-Functional Requirements (Architecture & Engineering)

* **REQ-NF1 (Gatekeeper & Rate Limiting):** All API calls must pass through a centralized API Gatekeeper using a FIFO queue to manage rate limits.
* **REQ-NF2 (Watchdog):** The system must implement a Keep-Alive/Watchdog mechanism. If an agent fails to respond within 15 seconds or returns invalid JSON, the Watchdog must intercept the error and force a retry.
* **REQ-NF3 (Context Engineering):** The system must utilize a "Write/Select" summarization strategy (Context Engineering Mixin) to compress older rounds and minimize token consumption.
* **REQ-NF4 (Observability):** The system must use rotating structured logs (e.g., max 20 files, 500 lines each) saving to `data/logs/app.log`.
* **REQ-NF5 (Security):** Zero hardcoded API keys. Keys must be injected via `.env`.

## 6. Assumptions, Dependencies, & Constraints
* **Dependencies:** `google-generativeai` SDK, `uv` package manager, Python 3.10+.
* **Constraints:** Must use standard `logging.handlers` for log rotation. All UI elements are restricted to the terminal (no external GUI required).
* **Assumptions:** The Gemini API will remain available during the test window. 

## 7. Timeline & Milestones
* **Phase 1:** Infrastructure & Planning Docs
* **Phase 2:** Configuration & Rotating Logs
* **Phase 3:** Gatekeeper & SDK Entry Point
* **Phase 4:** Agent OOP Mixins & JSON Protocols
* **Phase 5:** Judge Orchestrator & Watchdog
* **Phase 6:** CLI Integration & Cost Analysis Notebook