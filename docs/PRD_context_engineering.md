# PRD: Context Window Engineering (Incremental JSON State Strategy)

## 1. Overview & Problem Statement

In a 10-round multi-agent debate, passing the full conversation history to the LLM on every turn results in exponential token growth.

This causes:

- High API costs
- Increased latency
- Context window degradation
- Instruction forgetting ("lost in the middle" phenomenon)

---

# 2. Proposed Mechanism: Incremental JSON Rolling State

To solve context explosion, the system abandons raw string summarization and instead implements an incremental rolling state managed by the `ContextEngineeringMixin`.

---

## 2.1 The Incremental Update Loop

Instead of repeatedly summarizing an ever-growing history string, memory updates follow the deterministic formula:

```text
Old JSON Memory + New Debate Turn -> Updated JSON Memory
```

This guarantees stable memory growth and predictable token usage.

---

## 2.2 The Lean JSON Schema

Memory is strictly constrained to a strategic JSON schema.

The agent only retains information relevant to winning the debate while discarding fluff, repetition, and rhetorical noise.

### Memory Schema

```json
{
  "my_arguments": [
    "List of claims I have made"
  ],
  "opponent_arguments": [
    "List of claims the opponent has made"
  ],
  "verified_facts": [
    "Facts proven via live search"
  ],
  "invalidated_claims": [
    "Opponent claims we have proven false"
  ]
}
```

### Design Goals

- Preserve strategic continuity
- Prevent exponential context growth
- Retain verified factual state
- Track debunked arguments
- Enable efficient counterargument retrieval

---

# 3. Architecture & Constraints

## Location

```text
src/services/agent_mixins.py -> ContextEngineeringMixin
```

---

## Trigger

The mixin is automatically invoked by the `BaseAgent` at the end of each debate round to update the agent's internal rolling memory state.

---

## Fallback Strategy

If:

- The summarization/update API call fails
- Invalid JSON is produced

the system must gracefully recover by reverting to the previous round's last valid JSON state.

This prevents catastrophic memory corruption or total strategic loss.

### Fallback Rule

```text
Last Known Valid JSON State -> Restore
```

---

# 4. Success Criteria

## Flat Token Curve

The `prompt_token_count` across all 10 debate rounds must remain effectively flat.

### Complexity Target

The memory system must scale at:

```text
O(1)
```

rather than exponentially.

---

## Strategic Integrity

The agent must successfully use the `invalidated_claims` array to:

- Detect repeated opponent arguments
- Prevent recycled debunked claims
- Maintain long-term strategic consistency across rounds