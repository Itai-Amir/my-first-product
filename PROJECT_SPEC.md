# PROJECT IMPLEMENTATION PLAN — AI Agent Matching System

This document defines the **complete feature-by-feature implementation plan**
for the AI Agent Matching System.

Each feature strictly follows the **Feature Template contract** and is designed
to be implemented independently, deterministically, and without scope leakage.

---

# Feature 001: Persist Candidate Knowledge Pack

## Capability
Persist the candidate’s structured Knowledge Pack as the single deterministic source of truth.

## Context
Owned by the Candidate Agent.
Consumed by all downstream evaluation and negotiation features.

## Inputs
- Structured Knowledge Pack (JSON)
- Source: Candidate onboarding process
- Required: Yes

## Outputs
- Persisted Knowledge Pack artifact
- Destination: Local storage / DB
- Deterministic: Yes

## Constraints (Non-Negotiable)
- No schema changes
- No enrichment
- Deterministic serialization only

## Acceptance Criteria
- Save/load round-trip is byte-identical
- No unrelated files modified
- All tests pass

## Out of Scope
- Validation beyond schema
- Tagging or inference

## Failure Modes
- Invalid schema → fail fast

## Validation
- Save/load snapshot test

---

# Feature 002: Load Knowledge Pack as Immutable Source

## Capability
Load persisted Knowledge Pack into memory as a read-only structure.

## Context
Consumed by all Candidate Agent logic.

## Inputs
- Persisted Knowledge Pack artifact

## Outputs
- Immutable in-memory representation

## Constraints (Non-Negotiable)
- No mutation allowed
- No caching

## Acceptance Criteria
- Mutation attempts fail
- Identical reloads

## Out of Scope
- Partial loading

## Failure Modes
- Missing artifact → error

## Validation
- Immutability tests

---

# Feature 010: Evaluate Hard Gates

## Capability
Evaluate AI-core, work-mode, and compensation hard constraints.

## Context
First evaluation step inside Candidate Agent.

## Inputs
- Job Profile
- Knowledge Pack

## Outputs
- Pass/Fail decision
- Failure reasons

## Constraints (Non-Negotiable)
- No heuristics
- Fixed rule order

## Acceptance Criteria
- Immediate reject on failure

## Out of Scope
- Scoring

## Failure Modes
- Missing required fields

## Validation
- Gate-specific tests

---

# Feature 011: Compute Match Score

## Capability
Compute weighted deterministic match score.

## Context
Executed only after hard gates pass.

## Inputs
- Job Profile
- Knowledge Pack

## Outputs
- Match score
- Category breakdown

## Constraints (Non-Negotiable)
- Fixed weights
- Deterministic math

## Acceptance Criteria
- Identical input → identical score

## Out of Scope
- Ranking

## Failure Modes
- Missing category → zero score

## Validation
- Golden dataset tests

---

# Feature 012: Generate Match Evaluation Response

## Capability
Produce structured evaluation response.

## Context
Final output of Candidate Agent.

## Inputs
- Gate result
- Score breakdown

## Outputs
- Evaluation JSON

## Constraints (Non-Negotiable)
- No text generation

## Acceptance Criteria
- Schema compliant output

## Out of Scope
- UX formatting

## Failure Modes
- Inconsistent input states

## Validation
- Snapshot validation

---

# Feature 020: Normalize Job Description

## Capability
Convert recruiter input into structured Job Profile.

## Context
Owned by Recruiter Interface.

## Inputs
- Pasted JD
- Recruiter answers

## Outputs
- Normalized Job Profile

## Constraints (Non-Negotiable)
- No inference

## Acceptance Criteria
- Deterministic normalization

## Out of Scope
- NLP enrichment

## Failure Modes
- Missing required recruiter answers

## Validation
- Mapping tests

---

# Feature 021: Guided Recruiter Questions

## Capability
Ask fixed clarifying questions when needed.

## Context
Recruiter Interface only.

## Inputs
- Missing Job Profile fields

## Outputs
- Structured answers

## Constraints (Non-Negotiable)
- Fixed question set

## Acceptance Criteria
- Questions shown only when required

## Out of Scope
- UX design

## Failure Modes
- Incomplete answers

## Validation
- Conditional flow tests

---

# Feature 030: Evaluate Compensation Overlap

## Capability
Check numeric overlap between candidate and company compensation.

## Context
Negotiation Agent entry point.

## Inputs
- Candidate compensation expectations
- Company compensation band

## Outputs
- Accept / Counter / Reject

## Constraints (Non-Negotiable)
- Numeric only

## Acceptance Criteria
- Correct overlap detection

## Out of Scope
- Equity valuation

## Failure Modes
- Missing ranges

## Validation
- Boundary tests

---

# Feature 031: Generate Counter Proposal

## Capability
Generate minimum required counter adjustments.

## Context
Negotiation Agent.

## Inputs
- Failed overlap evaluation

## Outputs
- Counter proposal JSON

## Constraints (Non-Negotiable)
- Requirements only

## Acceptance Criteria
- No optional asks

## Out of Scope
- Tone or messaging

## Failure Modes
- Impossible counter

## Validation
- Schema checks

---

# Feature 040: Orchestrate Evaluation Fan-Out

## Capability
Dispatch job profiles to candidate agents and collect results.

## Context
Orchestrator core.

## Inputs
- Job Profile
- Candidate endpoints

## Outputs
- Evaluation list

## Constraints (Non-Negotiable)
- Deterministic ordering

## Acceptance Criteria
- All responses collected

## Out of Scope
- Ranking

## Failure Modes
- Candidate timeout

## Validation
- Multi-agent simulation

---

# Feature 041: Filter by Match Threshold

## Capability
Filter evaluations using fixed threshold.

## Context
Orchestrator decision step.

## Inputs
- Evaluation list

## Outputs
- Filtered candidates

## Constraints (Non-Negotiable)
- Fixed threshold

## Acceptance Criteria
- Correct filtering

## Out of Scope
- Overrides

## Failure Modes
- Empty result set

## Validation
- Threshold tests

---

# Feature 050: Trigger Human Escalation

## Capability
Emit escalation signal when all criteria met.

## Context
Final orchestration step.

## Inputs
- Successful match + negotiation

## Outputs
- Escalation signal

## Constraints (Non-Negotiable)
- Signal only

## Acceptance Criteria
- Trigger only on full alignment

## Out of Scope
- Notifications

## Failure Modes
- Partial alignment

## Validation
- End-to-end test
