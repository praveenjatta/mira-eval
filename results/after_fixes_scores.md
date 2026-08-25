# Mira Eval — Final Scores (Phase 5 Re-run)
**Date:** August 24, 2026  
**Judge Model:** gpt-4o-mini  
**Overall Average:** 0.87  
**Result:** 12 PASS / 0 FAIL

## Scores

| Test | Agent | Groundedness | Completeness | Accuracy | Overall | Verdict | Notes |
|------|-------|-------------|--------------|----------|---------|---------|-------|
| T1 | Planner | 1.00 | 1.00 | 1.00 | 1.00 | ✅ PASS | — |
| T2 | Planner | 0.00 | 1.00 | 1.00 | 0.67 | ✅ PASS | Guardrail test — groundedness=0 expected |
| T3 | Risk Assessor | 0.80 | 1.00 | 1.00 | 0.93 | ✅ PASS | — |
| T4 | Risk Assessor | 0.00 | 1.00 | 1.00 | 0.67 | ✅ PASS | Guardrail test — groundedness=0 expected |
| T5 | Status Reporter | 1.00 | 1.00 | 1.00 | 1.00 | ✅ PASS | — |
| T6 | Status Reporter | 0.00 | 1.00 | 1.00 | 0.67 | ✅ PASS | Guardrail test — groundedness=0 expected |
| T7 | Risk Assessor | 1.00 | 1.00 | 1.00 | 1.00 | ✅ PASS | — |
| T8 | Milestone Tracker | 1.00 | 1.00 | 1.00 | 1.00 | ✅ PASS | — |
| T9 | Planner | 0.00 | 1.00 | 1.00 | 0.67 | ✅ PASS | Guardrail test — groundedness=0 expected |
| T10 | Status Reporter | 1.00 | 1.00 | 1.00 | 1.00 | ✅ PASS | — |
| T11 | Milestone Tracker | 0.80 | 1.00 | 0.90 | 0.90 | ✅ PASS | — |
| T12 | Stakeholder Update | 1.00 | 0.80 | 1.00 | 0.93 | ✅ PASS | — |

## Score Explanation

**Why overall is 0.87 (lower than previous 0.99):**

The test dataset now uses the **official eval_mira_inputs.txt** test cases which include 4 guardrail tests (T2, T4, T6, T9). These tests intentionally send vague/insufficient input to verify the agents correctly refuse and ask for more information. For guardrail tests, groundedness=0 is **expected and correct behavior** — the agent should NOT be grounded in project data when refusing a vague request.

| Test Type | Count | Avg Score |
|-----------|-------|-----------|
| Grounded responses (T1, T3, T5, T7, T8, T10, T11, T12) | 8 | 0.97 |
| Guardrail responses (T2, T4, T6, T9) | 4 | 0.67 |
| **All 12 tests** | **12** | **0.87** |

## Fix Log
- **T5** — Status Reporter: Added BLOCKED TASK RULE + SPRINT FILTER RULE + DOUBLE CHECK RULE → 0.17 → 1.00 ✅
- **T10** — Status Reporter: Added Blocked count to summary rule → Now correctly reports Blocked:1, Total:25 ✅
- **T11** — Milestone Tracker: Fixed MESSAGE 2 expression + updated CRITICAL GUARDRAIL → Now returns milestones ✅
- **T12** — Stakeholder Update: Added SPRINT SCOPE RULE + BLOCKER RULE → 0.63 → 0.93 ✅

## Summary
- All fixes achieved with **Lever 1 — Prompt Engineering only**
- No need for Levels 2, 3, 4, or Fine-Tuning
- 12/12 PASS on official test dataset ✅
- Langfuse observability integrated — 12 traces captured ✅
