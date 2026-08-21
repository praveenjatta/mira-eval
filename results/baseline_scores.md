# Mira Eval — Baseline Scores
**Date:** August 21, 2026  
**Judge Model:** gpt-4o-mini  
**Overall Average:** 0.89  
**Result:** 10 PASS / 2 FAIL

## Scores

| Test | Agent | Groundedness | Completeness | Accuracy | Overall | Verdict |
|------|-------|-------------|--------------|----------|---------|---------|
| T1 | Planner | 1.00 | 1.00 | 1.00 | 1.00 | ✅ PASS |
| T2 | Risk Assessor | 1.00 | 0.80 | 1.00 | 0.93 | ✅ PASS |
| T3 | Risk Assessor | 1.00 | 1.00 | 1.00 | 1.00 | ✅ PASS |
| T4 | Planner | 1.00 | 1.00 | 1.00 | 1.00 | ✅ PASS |
| T5 | Status Reporter | 0.50 | 0.00 | 0.00 | 0.17 | ❌ FAIL |
| T6 | Status Reporter | 1.00 | 1.00 | 1.00 | 1.00 | ✅ PASS |
| T7 | Risk Assessor | 1.00 | 1.00 | 1.00 | 1.00 | ✅ PASS |
| T8 | Milestone Tracker | 1.00 | 1.00 | 1.00 | 1.00 | ✅ PASS |
| T9 | Milestone Tracker | 1.00 | 1.00 | 1.00 | 1.00 | ✅ PASS |
| T10 | Risk Assessor | 1.00 | 1.00 | 1.00 | 1.00 | ✅ PASS |
| T11 | Milestone Tracker | 1.00 | 1.00 | 1.00 | 1.00 | ✅ PASS |
| T12 | Stakeholder Update | 1.00 | 0.40 | 0.50 | 0.63 | ❌ FAIL |

## Failures

### T5 — Status Reporter (0.17)
- Missing T024 BLOCKED task
- Incorrectly states "no blocked tasks"
- Fix: Lever 1 — Prompt Engineering

### T12 — Stakeholder Update (0.63)
- Missing T024 blocker mention
- Contains "no significant blockers" (must-not-contain violation)
- Sprint 1 bleed-in
- Fix: Lever 1 — Prompt Engineering