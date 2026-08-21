# mira-eval

> LLM-judge evaluation framework for **Mira — Project Intelligence Assistant**  
> Built as part of the Applied Agentic AI for PMs/TPMs capstone project

---

## Overview

`mira-eval` is a Python-based evaluation framework that uses **GPT-4o-mini as an LLM judge** to score the outputs of Mira, a multi-agent AI system built in n8n. It evaluates all 12 baseline test cases against a ground truth dataset across 3 metrics: Groundedness, Completeness, and Accuracy.

---

## Project Structure

```
mira-eval/
├── eval_mira.py                 # Main evaluation script (LLM judge)
├── ground_truth.json            # 12 test cases with expected outputs & criteria
├── requirements.txt             # Python dependencies
├── results/
│   ├── eval_results.json        # Raw scores from LLM judge
│   ├── baseline_scores.md       # Scores before prompt engineering fixes
│   └── after_fixes_scores.md    # Scores after prompt engineering fixes
└── .gitignore
```

---

## Evaluation Metrics

Each test case is scored on 3 dimensions:

| Metric | Description |
|--------|-------------|
| **Groundedness** | Is the output grounded in actual project data? |
| **Completeness** | Does it cover all expected keywords and pass criteria? |
| **Accuracy** | Is the information correct? Does it avoid must-not-contain items? |

Overall score = average of all 3 metrics (0.0 to 1.0 scale).

---

## Results Summary

| Phase | Overall Score | Pass Rate |
|-------|--------------|-----------|
| Baseline (before fixes) | 0.89 | 10 / 12 |
| After Prompt Engineering | **0.99** | **12 / 12** |

### Failures Fixed via Prompt Engineering

| Test | Agent | Issue | Fix Applied | Score Change |
|------|-------|-------|-------------|-------------|
| T5 | Status Reporter | Missed T024 BLOCKED task; said "no blocked tasks" | Added BLOCKED TASK RULE + SPRINT FILTER RULE to system prompt | 0.17 → 1.00 |
| T12 | Stakeholder Update | Sprint 1 bleed-in + missed T024 blocker | Added SPRINT SCOPE RULE + BLOCKER RULE + updated guardrail | 0.63 → 1.00 |

### Fix Ladder Approach

Fixes were applied using a 5-level optimization ladder:

| Level | Approach | Used? |
|-------|----------|-------|
| L1 | Prompt Engineering | ✅ Yes — solved both failures |
| L2 | Pipeline Restructuring | Not needed |
| L3 | Model Swapping | Not needed |
| L4 | RAG / Better Grounding | Not needed |
| L5 | Fine-Tuning | Not needed |

Both T5 and T12 were fully resolved at **Lever 1 — Prompt Engineering only**.

---

## Agents Evaluated

| Agent | Tests | Final Score |
|-------|-------|-------------|
| Planner | T1, T4 | 1.00 |
| Risk Assessor | T2, T3, T7, T10 | 0.93 – 1.00 |
| Status Reporter | T5, T6 | 1.00 (after fix) |
| Milestone Tracker | T8, T9, T11 | 1.00 |
| Stakeholder Update | T12 | 1.00 (after fix) |

---

## Setup

```bash
# Clone the repo
git clone https://github.com/praveenjatta/mira-eval.git
cd mira-eval

# Create virtual environment (Python 3.11)
python3.11 -m venv venv --without-pip
source venv/bin/activate
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python get-pip.py

# Install dependencies
python3.11 -m pip install -r requirements.txt

# Add your OpenAI API key
echo "OPENAI_API_KEY=your-key-here" > .env
```

---

## Usage

```bash
python3.11 eval_mira.py
```

The script will:

1. Load all 12 test cases from `ground_truth.json`
2. Score each Mira output using GPT-4o-mini as LLM judge
3. Print a detailed results table to console
4. Save raw scores to `results/eval_results.json`

### Sample Output

```
============================================================
MIRA EVALUATION REPORT — LLM Judge (gpt-4o-mini)
============================================================
Evaluating T1 — Planner...
✅ T1 | Groundedness: 1.00 | Completeness: 1.00 | Accuracy: 1.00 | Overall: 1.00 | PASS
...
✅ T12 | Groundedness: 1.00 | Completeness: 1.00 | Accuracy: 1.00 | Overall: 1.00 | PASS
============================================================
OVERALL AVERAGE SCORE: 0.99
TESTS EVALUATED: 12
============================================================
```

---

## Tech Stack

| Tool | Purpose |
|------|---------|
| Python 3.11 | Runtime |
| DeepEval | LLM evaluation framework |
| OpenAI GPT-4o-mini | LLM judge model |
| python-dotenv | Environment variable management |

---

## Ground Truth Dataset

The `ground_truth.json` file contains 12 test cases covering all 5 Mira agents. Each test case includes:

- `test_id` — unique identifier (T1–T12)
- `agent` — which Mira agent is being evaluated
- `user_request` — the input sent to Mira
- `expected_keywords` — keywords that must appear in the output
- `must_not_contain` — phrases that must not appear
- `pass_criteria` — plain English description of what a passing response looks like

---

## Related Projects

- [mira-project-intelligence-agent](https://github.com/praveenjatta/mira-project-intelligence-agent) — The main Mira n8n workflow (capstone project)

---

## Author

**Praveen Kumar Jatta** — Senior TPM | PMP® CSPO® SMC®

[JattaAI](https://jattaai.com) | [LinkedIn](https://linkedin.com/in/praveenjatta) | [GitHub](https://github.com/praveenjatta)
