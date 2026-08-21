# 🧠 mira-eval

An LLM-judge evaluation framework for **Mira — Project Intelligence Assistant**, a multi-agent AI system built in n8n. Uses GPT-4o-mini as an automated judge to score outputs across 12 test cases against a ground truth dataset.

---

## 🧩 The Problem It Solves

How do you know if your AI agent is actually working? Manual review of 12 test cases across 5 specialized agents is slow, inconsistent, and hard to repeat. `mira-eval` automates the entire evaluation loop — load the outputs, run the judge, get objective scores, fix the prompts, repeat.

One script. Twelve tests. Three metrics. Fully automated.

---

## 🔬 How It Works

```
ground_truth.json         → 12 test cases with expected keywords & pass criteria
    ↓
eval_mira.py              → Loads test cases + Mira outputs
    ↓
LLM Judge (gpt-4o-mini)   → Scores each output on 3 metrics
    ↓
Results printed to console + saved to results/eval_results.json
    ↓
Fix prompts in n8n → Re-run → Re-score → Repeat
```

---

## 🏗️ Project Structure

| File / Folder | Description |
|---------------|-------------|
| `eval_mira.py` | Main evaluation script — LLM judge logic |
| `ground_truth.json` | 12 test cases with expected outputs & pass criteria |
| `requirements.txt` | Python dependencies |
| `results/eval_results.json` | Raw scores from LLM judge (latest run) |
| `results/baseline_scores.md` | Scores before any prompt engineering fixes |
| `results/after_fixes_scores.md` | Scores after all prompt engineering fixes |

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

| Phase | Overall Score | Pass Rate |
|-------|:------------:|:---------:|
| 🔴 Baseline (before fixes) | 0.89 | 10 / 12 |
| 🟢 After Prompt Engineering | **0.99** | **12 / 12** |

---

## 🔧 Failures Fixed

### ❌ T5 — Status Reporter (0.17 → ✅ 1.00)

**Issue:** Agent reported "no blocked tasks" for Sprint 3 — missed T024 (Security review, BLOCKED).

**Fix (Lever 1 — Prompt Engineering):**
- Added `BLOCKED TASK RULE` — scan entire task board before finalizing any report
- Added `SPRINT FILTER RULE` — sprint-specific counts must reflect only that sprint's tasks

---

### ❌ T12 — Stakeholder Update (0.63 → ✅ 1.00)

**Issue:** Included Sprint 1 tasks (bleed-in), said "no significant blockers" — missed T024.

**Fix (Lever 1 — Prompt Engineering):**
- Added `SPRINT SCOPE RULE` — include only tasks whose Sprint field exactly matches
- Added `BLOCKER RULE` — always surface BLOCKED tasks regardless of sprint requested
- Updated `CRITICAL GUARDRAIL` — only trigger on truly empty project data

---

## 🪜 Fix Ladder Applied

| Level | Approach | Status |
|-------|----------|--------|
| **L1** | 🔧 Prompt Engineering | ✅ Used — solved both failures |
| L2 | 🔗 Pipeline Restructuring | ⏭️ Not needed |
| L3 | 🔄 Model Swapping | ⏭️ Not needed |
| L4 | 📚 RAG / Better Grounding | ⏭️ Not needed |
| L5 | 🎯 Fine-Tuning | ⏭️ Not needed |

> Both T5 and T12 were fully resolved at **Lever 1 — Prompt Engineering only**. No fine-tuning required.

---

## 🤖 Agents Evaluated

| Agent | Test IDs | Final Score |
|-------|----------|:-----------:|
| 🗓️ Planner | T1, T4 | 1.00 |
| ⚠️ Risk Assessor | T2, T3, T7, T10 | 0.93 – 1.00 |
| 📋 Status Reporter | T5, T6 | 1.00 ✅ (fixed) |
| 🏁 Milestone Tracker | T8, T9, T11 | 1.00 |
| 📧 Stakeholder Update | T12 | 1.00 ✅ (fixed) |

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

**Prerequisites:**
- Python 3.11
- OpenAI API key

**Setup Steps:**

1. Clone the repo:
```bash
git clone https://github.com/praveenjatta/mira-eval.git
cd mira-eval
```

2. Create virtual environment:
```bash
python3.11 -m venv venv --without-pip
source venv/bin/activate
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python get-pip.py
```

3. Install dependencies:
```bash
python3.11 -m pip install -r requirements.txt
```

4. Add your OpenAI API key:
```bash
echo "OPENAI_API_KEY=your-key-here" > .env
```

5. Run the evaluation:
```bash
python3.11 eval_mira.py
```

---

## 📋 Sample Output

```
============================================================
MIRA EVALUATION REPORT — LLM Judge (gpt-4o-mini)
============================================================
Evaluating T1 — Planner...
✅ T1 | Groundedness: 1.00 | Completeness: 1.00 | Accuracy: 1.00 | Overall: 1.00 | PASS
Evaluating T5 — Status Reporter...
✅ T5 | Groundedness: 1.00 | Completeness: 1.00 | Accuracy: 1.00 | Overall: 1.00 | PASS
Evaluating T12 — Stakeholder Update...
✅ T12 | Groundedness: 1.00 | Completeness: 1.00 | Accuracy: 1.00 | Overall: 1.00 | PASS
============================================================
OVERALL AVERAGE SCORE: 0.99
TESTS EVALUATED: 12
============================================================
Results saved to results/eval_results.json
```

---

## 🔑 Key Design Decisions

**GPT-4o-mini as judge** — Fast, cost-effective, and consistent. Temperature set to 0 for deterministic scoring across runs.

**3-metric scoring** — Groundedness, Completeness, and Accuracy each capture a different failure mode. A single score would mask partial failures.

**must-not-contain guardrail** — Certain phrases (like "no blocked tasks") are hard failures regardless of other quality signals. The judge checks these explicitly.

**Fix ladder discipline** — Prompt engineering is always tried first before reaching for heavier solutions. This keeps the system simple and maintainable.

**Separation of concerns** — Evaluation lives in its own repo (`mira-eval`) separate from the workflow (`mira-project-intelligence-agent`). Each can evolve independently.

---

## 🔗 Related Projects

- 🤖 [mira-project-intelligence-agent](https://github.com/praveenjatta/mira-project-intelligence-agent) — The main Mira n8n workflow (capstone project)

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
