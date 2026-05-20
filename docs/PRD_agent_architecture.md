# PRD: OOP Agent Architecture, Skills & JSON Protocol

## 1. Overview & Problem Statement

Hardcoding three distinct agents leads to massive code duplication, violating the DRY (Don't Repeat Yourself) principle and the strict OOP standards. Furthermore, unstructured text responses break the orchestration loop.

We require a modular, inheritance-based architecture utilizing Mixins to provide skills (Function Calling), alongside a strict JSON protocol to guarantee stable Inter-Process Communication (IPC).

---

# 2. Class Inheritance & OOP Structure

The system utilizes a strict Object-Oriented design to prevent code duplication while allowing agents to possess asymmetric capabilities.

## 2.1 The Agent Hierarchy

### `BaseAgent`

The foundational class. It:

- Holds the reference to the `ApiGatekeeper`
- Manages local conversation history
- Strictly enforces the JSON output schema via the LLM API parameters

### `ProAgent` & `ConAgent`

Concrete implementations inheriting from:

- `BaseAgent`
- The required Mixins

They dynamically load their distinct personas from:

```text
config/instructions/agent_prompts.json
```

### `JudgeOrchestrator`

The mediator component.

It does **not** inherit from `BaseAgent` because its role is structural rather than conversational.

Responsibilities:

- Evaluates JSON responses based purely on persuasion
- Validates word counts
- Triggers the Watchdog upon failure
- Writes the final verdict

---

# 3. Skills & Mixins (Function Calling)

To ensure a robust, intelligent debate, cognitive capabilities and validation tools are injected into the agents via Mixins.

This modularity:

- Prevents code duplication
- Keeps the `BaseAgent` core logic pristine

---

## 3.1 Judge Skills (Rule Enforcement Mixins)

These tools empower the `JudgeOrchestrator` to programmatically and semantically validate debate rules without relying purely on standard LLM prompting.

### `WordCountValidatorMixin`

#### Tool

```python
validate_length(text: str)
```

#### Purpose

A deterministic Python function that:

- Strips punctuation
- Counts tokens/words
- Instantly fails the agent if the argument exceeds the strict 100-word limit

This saves API tokens by catching length violations before passing the text to the LLM Judge.

---

### `EngagementCheckerMixin`

#### Tool

```python
verify_rebuttal(
    current_argument: str,
    previous_opponent_argument: str
)
```

#### Purpose

Performs a semantic check ensuring the agent:

- Did not merely introduce a new point
- Actively addressed the opponent's previous claim

This satisfies the strict HW2 rebuttal requirement.

---

### `ToneAndEthicsMixin`

#### Tool

```python
check_tone(text: str)
```

#### Purpose

Scans arguments for:

- Ad hominem attacks
- Insults
- Un-parliamentary language

This enforces the "respectful debate" rule before arguments are officially accepted into the record.

---

## 3.2 Pro/Con Agent Skills: Advanced Reasoning (Plan-and-Solve)

These tools allow debating agents to construct stronger arguments using a multi-step Plan-and-Solve orchestration strategy integrating Live Google Search Grounding.

---

### `AdvancedReasoningMixin`

#### Core Subagent Workflows

---

### Workflow 1: Fact Checking (`fact_check`)

Instantly queries the live internet via Google Search Grounding.

Returns strict boolean-style tags:

- `[TRUE]`
- `[FALSE]`
- `[OPINION]`

Also returns URL sources to validate or debunk claims.

---

### Workflow 2: Draft & Validate (`look_for_arguments`)

#### Step A — Brainstorm

Generates new arguments without searching while referencing old memory to avoid duplication.

#### Step B — Validate

Spawns a search subagent to:

- Find real-world evidence
- Discard unprovable claims
- Return validated arguments with URLs

---

### Workflow 3: Strategic Counter-Offensive (`find_counterarguments`)

#### Step A

Fact-checks the opponent's premise.

If false:

- Halts immediately
- Attacks the factual error

#### Step B

Checks `ContextEngineeringMixin` memory state to determine whether a previous argument can serve as a counter.

Returns:

- `[FOUND]`
- `[NOT_FOUND]`

#### Step C

If not found in memory:

- Spawns a live web search
- Finds new counter-evidence

---

### `ContextEngineeringMixin`

#### Purpose

Implements an:

```text
O(1) Incremental JSON Rolling State Memory
```

Compresses historical debate rounds into a strategic schema:

```json
{
  "my_arguments": [],
  "opponent_arguments": [],
  "verified_facts": [],
  "invalidated_claims": []
}
```

This eliminates exponential token growth while retaining strategic integrity.

---

# 4. Inter-Process Communication (IPC) Protocol

Agents must never communicate via raw strings.

They use a strict JSON protocol to ensure the Judge can programmatically validate:

- Word counts
- Rule adherence
- Structural correctness

---

## 4.1 Pro/Con Agent Payload Schema

When the `ProAgent` or `ConAgent` generates an argument, it **must** return the following exact JSON structure:

```json
{
  "thought_process": "Internal reasoning on how to attack the opponent's claim.",
  "argument_summary": "A one-sentence summary of the main point.",
  "full_argument": "The <100 word response directed at the opponent.",
  "addressed_opponent_points": [
    "Specific point 1 that was addressed"
  ],
  "sources_used": [
    "URL from SearchMixin",
    "N/A"
  ]
}
```

---

## 4.2 Judge Validation Protocol

When the `JudgeOrchestrator` receives a payload, it validates the structure in the following order:

### JSON Parsing

Fails if the payload cannot be parsed into a valid Python dictionary.

### Word Count Check

Fails if:

```python
len(payload["full_argument"].split()) > 100
```

### Engagement Check

Fails if:

```python
addressed_opponent_points == []
```

---

## 4.3 Multi-Process Execution Paradigm

To ensure absolute isolation of agent states, the system follows a strict multi-process simulation architecture.

### Key Principles

- Each Agent and the Judge Orchestrator function as distinct logical processing threads
- Synchronization occurs via an orchestration loop controlled by the SDK
- Direct memory access between Pro and Con processes is prohibited
- Raw string sharing is forbidden

### IPC Transport

All IPC occurs asynchronously via:

```text
Structured JSON Message Buffers
```

Messages are passed exclusively through the Judge.

---

## 4.4 Judge Rejection & Correction Payload Schema

When validation fails (word limits, tone violations, malformed JSON, etc.), the `JudgeOrchestrator` interrupts execution and returns a structured rejection packet.

The agent's Watchdog wrapper must:

1. Parse the rejection packet
2. Append it as a temporary override in context
3. Immediately regenerate the response

### Rejection Packet Schema

```json
{
  "status": "REJECTED",
  "error_type": "WORD_COUNT_VIOLATION | TONE_VIOLATION | INVALID_JSON",
  "violation_details": "Your argument contained 124 words, exceeding the maximum allowed limit of 100 words.",
  "correction_instruction": "Regenerate your argument immediately. Ensure it is under 100 words while maintaining your exact strategic stance."
}
```

---

# 5. The Watchdog Integration & Resiliency

If:

- An agent fails Judge validation checks
- The `ApiGatekeeper` experiences a network timeout (15-second threshold)

the Watchdog mechanism activates.

---

## Watchdog Flow

### Catch

The `JudgeOrchestrator` catches:

- `JSONDecodeError`
- `TimeoutError`
- `ValidationError`

### Recover

The Watchdog logs failures to the rotating structured logger:

```text
data/logs/app.log
```

### Retry

The Watchdog appends a system warning to the failing agent prompt.

Example:

```text
System Error: Your previous response exceeded 100 words. Try again.
```

Then it forces a localized retry without crashing the `main.py` orchestration loop.

---

# 6. Success Criteria

## OOP Compliance

- Zero code duplication between:
  - Pro Agent prompt generation
  - Con Agent prompt generation
  - Gatekeeper execution logic

## Skill Execution

- `AdvancedReasoningMixin` successfully performs live search during debates

## JSON Reliability

- The system automatically recovers from:
  - Simulated JSON malformations
  - Network timeouts

via the Watchdog retry loop.