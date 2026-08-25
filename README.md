# 🧠 mira-eval

> LLM-judge evaluation framework for **Mira — Project Intelligence Assistant**  
> Built as part of the Applied Agentic AI for PMs/TPMs capstone project

---

## 🧩 Overview

`mira-eval` is a Python-based evaluation framework that uses **GPT-4o-mini as an LLM judge** to score the outputs of Mira, a multi-agent AI system built in n8n. It evaluates all 12 official test cases against a ground truth dataset across 3 metrics: Groundedness, Completeness, and Accuracy.

---

## 🏗️ Project Structure

```
mira-eval/
├── eval_mira.py                 # Main evaluation script (LLM judge)
├── ground_truth.json            # 12 test cases with expected outputs & pass criteria
├── requirements.txt             # Python dependencies
├── results/
│   ├── eval_results.json        # Raw scores from LLM judge (latest run)
│   ├── baseline_scores.md       # Scores before prompt engineering fixes
│   └── after_fixes_scores.md    # Final scores after all fixes
└── .gitignore
```

---

## 📊 Evaluation Metrics

Each test case is scored on 3 dimensions (0.0 to 1.0):

| Metric | Description |
|--------|-------------|
| 🎯 **Groundedness** | Is the output grounded in actual project data? No hallucinations? |
| ✅ **Completeness** | Does it cover all expected keywords and meet the pass criteria? |
| 🔍 **Accuracy** | Is the information correct? Does it avoid must-not-contain phrases? |

> Overall score = average of all 3 metrics

---

## 📈 Results Summary

| Phase | Test Dataset | Overall Score | Pass Rate |
|-------|-------------|:------------:|:---------:|
| 🔴 Baseline (before fixes) | Custom outputs | 0.89 | 10 / 12 |
| 🟢 After Prompt Engineering | Official test inputs | **0.87** | **12 / 12** |

### Why 0.87 and not higher?

The final evaluation uses the **official test dataset** (`eval_mira_inputs.txt`) which includes **4 guardrail tests** (T2, T4, T6, T9). These tests send vague/insufficient input to verify agents correctly refuse and ask for more information.

For guardrail tests, **groundedness=0 is expected and correct** — the agent should NOT be grounded in project data when refusing a vague request.

| Test Type | Count | Avg Score |
|-----------|-------|-----------|
| Grounded responses (T1, T3, T5, T7, T8, T10, T11, T12) | 8 | 0.97 |
| Guardrail responses (T2, T4, T6, T9) | 4 | 0.67 |
| **All 12 tests** | **12** | **0.87** |

---

## 🔧 Failures Fixed via Prompt Engineering

| Test | Agent | Issue | Fix | Score Change |
|------|-------|-------|-----|-------------|
| T5 | Status Reporter | Missed T024 BLOCKED task | Added BLOCKED TASK RULE + SPRINT FILTER RULE + DOUBLE CHECK RULE | 0.17 → 1.00 |
| T10 | Status Reporter | Missing Blocked count in summary | Added Blocked count to summary rule | Fixed |
| T11 | Milestone Tracker | INSUFFICIENT INFORMATION for milestone query | Fixed Message 2 expression + updated CRITICAL GUARDRAIL | Fixed |
| T12 | Stakeholder Update | Sprint 1 bleed-in + missed blocker | Added SPRINT SCOPE RULE + BLOCKER RULE | 0.63 → 0.93 |

---

## 🪜 Fix Ladder Applied

| Level | Approach | Status |
|-------|----------|--------|
| **L1** | 🔧 Prompt Engineering | ✅ Used — solved all failures |
| L2 | 🔗 Pipeline Restructuring | ⏭️ Not needed |
| L3 | 🔄 Model Swapping | ⏭️ Not needed |
| L4 | 📚 RAG / Better Grounding | ⏭️ Not needed |
| L5 | 🎯 Fine-Tuning | ⏭️ Not needed |

> All failures resolved at **Lever 1 — Prompt Engineering only**.

---

## 🤖 Agents Evaluated

| Agent | Test IDs | Final Score |
|-------|----------|:-----------:|
| 🗓️ Planner | T1, T2, T9 | 1.00 / 0.67 / 0.67 |
| ⚠️ Risk Assessor | T3, T4, T7 | 0.93 / 0.67 / 1.00 |
| 📋 Status Reporter | T5, T6, T10 | 1.00 / 0.67 / 1.00 |
| 🏁 Milestone Tracker | T8, T11 | 1.00 / 0.90 |
| 📧 Stakeholder Update | T12 | 0.93 |

---

## 🛠️ Tech Stack

| Tool | Purpose |
|------|---------|
| Python 3.11 | Runtime |
| DeepEval | LLM evaluation framework |
| OpenAI GPT-4o-mini | LLM judge model |
| python-dotenv | Environment variable management |

---

## 🚀 Setup & Usage

**1. Clone the repo:**
```bash
git clone https://github.com/praveenjatta/mira-eval.git
cd mira-eval
```

**2. Create virtual environment:**
```bash
python3.11 -m venv venv --without-pip
source venv/bin/activate
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python get-pip.py
```

**3. Install dependencies:**
```bash
python3.11 -m pip install -r requirements.txt
```

**4. Add your OpenAI API key:**
```bash
echo "OPENAI_API_KEY=your-key-here" > .env
```

**5. Run evaluation:**
```bash
python3.11 eval_mira.py
```

---

## 📋 Sample Output

```
============================================================
MIRA EVALUATION REPORT — LLM Judge (gpt-4o-mini)
============================================================
✅ T1  | Groundedness: 1.00 | Completeness: 1.00 | Accuracy: 1.00 | Overall: 1.00 | PASS
✅ T2  | Groundedness: 0.00 | Completeness: 1.00 | Accuracy: 1.00 | Overall: 0.67 | PASS
✅ T5  | Groundedness: 1.00 | Completeness: 1.00 | Accuracy: 1.00 | Overall: 1.00 | PASS
✅ T12 | Groundedness: 1.00 | Completeness: 0.80 | Accuracy: 1.00 | Overall: 0.93 | PASS
============================================================
OVERALL AVERAGE SCORE: 0.87
TESTS EVALUATED: 12
============================================================
```

---

## 🔗 Related Projects

- 🤖 [mira-project-intelligence-agent](https://github.com/praveenjatta/mira-project-intelligence-agent) — The main Mira n8n workflow

---

## 👤 Author

**Praveen Kumar Jatta** — Senior Technical Program Manager | AI Automation Consultant

- 🌐 [jattaai.com](https://jattaai.com)
- 💼 [linkedin.com/in/praveenjatta](https://linkedin.com/in/praveenjatta)
- 🐙 [github.com/praveenjatta](https://github.com/praveenjatta)
- 📅 [Book a free discovery call](https://calendly.com/praveenjatta/free-ai-automation-discovery-call)

---

## 📄 License

MIT License — free to use and modify with attribution.
