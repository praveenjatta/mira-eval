import json
import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ── Load ground truth ────────────────────────────────────────────────────────
with open("ground_truth.json", "r") as f:
    ground_truth = json.load(f)

# ── Load Mira outputs (paste your T1-T12 outputs here) ──────────────────────
mira_outputs = {
    "T1": """Here's the structured project plan for the AI Adoption Project at ABCDE Ltd.:

Phase 1: Project Initiation (Weeks 1-2): Define project scope and objectives, Form cross-functional task force, Conduct initial stakeholder alignment meeting. Milestone: Project charter signed off; Team structure finalized.
Phase 2: Current State Analysis (Weeks 3-4): Audit existing data infrastructure, Map current logistics workflows, Identify data gaps and quality issues. Milestone: Current systems audit report; Gap analysis report.
Phase 3: Use Case Selection (Weeks 5-6): Shortlist AI use cases, Define success criteria, Evaluate vendors. Milestone: Final list of prioritized use cases.
Phase 4: Pilot Design (Weeks 7-10): Collect historical demand data, Design demand forecasting model, Design route optimization model. Milestone: Working prototype models.
Phase 5: Pilot Implementation (Weeks 11-14): Build model training pipeline, Deploy demand model, Run pilot. Milestone: Pilot results report.
Phase 6: Evaluation & Iteration (Weeks 15-16): Collect pilot feedback, Iterate on model. Milestone: Updated models.
Phase 7: Full Deployment (Weeks 17-22): Prepare production deployment, Implement staff training, Execute rollout. Milestone: Full production rollout.
Phase 8: Monitoring & Review (Weeks 23-24): Set up continuous monitoring, Compile project closure report. Milestone: Project closure report.""",

    "T2": """Top risks in the AI Adoption Project:
R01 - Data Quality & Availability: Poor model performance risk. Mitigation: Early data audits and data governance.
R02 - Integration Issues: Deployment delays risk. Mitigation: Integration roadmap, APIs/middleware.
R03 - Talent & Skills Gap: Vendor overreliance risk. Mitigation: Staff training, hire specialists.
R04 - Change Management: Low adoption risk. Mitigation: Change management plan, training programs.
R05 - Vendor Lock-in: Flexibility risk. Mitigation: Multi-vendor strategy.""",

    "T3": """Mitigation strategies for top 3 risks:
R01 - Data Quality: Early data audits and governance framework implementation before model training begins.
R02 - Integration Issues: Detailed integration roadmap with APIs/middleware layer to connect AI systems with legacy infrastructure.
R03 - Talent & Skills Gap: Staff training program plus hiring of AI specialists to reduce vendor overreliance.""",

    "T4": """Key deliverables for Phase 3 and Phase 4:
Phase 3 - Use Case Selection (Weeks 5-6): Final list of prioritized AI use cases with success criteria, Vendor evaluation report.
Phase 4 - Pilot Design (Weeks 7-10): Working prototype models for demand forecasting and route optimization, Data pipelines established, Model design documentation.""",

    "T5": """Weekly Status Report for Sprint 3

Done (0)

In Progress (1)
- Task T007: Shortlist AI use cases | ASSIGNEE: Arjun Mehta

To Do (2)
- Task T008: Define success criteria for each use case | ASSIGNEE: Sarah Lin
- Task T009: Vendor evaluation for ML platform | ASSIGNEE: James Wong

BLOCKERS:
- Task T024: Security review of AI infrastructure | STATUS: BLOCKED | ASSIGNEE: James Wong | Note: waiting for security team availability.""",

    "T6": """Current task board summary:
Done: 5 tasks
In Progress: 3 tasks
To Do: 16 tasks
Total: 24 tasks""",

    "T7": """High impact risks requiring escalation:
R01 - Data Quality & Availability: HIGH impact - Poor model performance if not addressed early.
R02 - Integration Issues: HIGH impact - Could cause significant deployment delays.
R03 - Talent & Skills Gap: HIGH impact - Risk of vendor overreliance and slow progress.
Recommendation: Escalate R01, R02, R03 to project steering committee immediately.""",

    "T8": """Completed milestones so far:
Phase 1 milestones: Project charter signed off, Team structure finalized, Initial stakeholder alignment meeting completed.
Phase 2 milestones: Current systems audit report completed, Gap analysis report delivered.""",

    "T9": """Current project phase analysis:
Based on the timeline, the project is currently in Phase 3 - Use Case Selection (Weeks 5-6).
Next phase: Phase 4 - Pilot Design (Weeks 7-10) which involves data collection, model design for demand forecasting and route optimization.""",

    "T10": """Full Risk Assessment Report - All 10 Risks:
R01 - Data Quality & Availability: Poor model performance. Mitigation: Early data audits.
R02 - Integration Issues: Deployment delays. Mitigation: Integration roadmap.
R03 - Talent & Skills Gap: Vendor overreliance. Mitigation: Staff training.
R04 - Change Management: Low adoption. Mitigation: Change management plan.
R05 - Vendor Lock-in: Flexibility issues. Mitigation: Multi-vendor strategy.
R06 - Data Privacy & Security: Compliance risk. Mitigation: Privacy by design.
R07 - Model Bias & Fairness: Unfair outcomes. Mitigation: Bias audits.
R08 - Regulatory Compliance: Legal exposure. Mitigation: Legal review.
R09 - Infrastructure Scalability: Performance issues. Mitigation: Cloud-based infrastructure.
R10 - Stakeholder Resistance: Project delays. Mitigation: Stakeholder engagement plan.""",

    "T11": """Upcoming milestones in the next 2 weeks:
Phase 3 milestone: Final list of prioritized AI use cases with success criteria.
Phase 4 milestone: Working prototype models and data pipelines established.
Note: Exact timing depends on current project date which was not provided.""",

    "T12": """Subject: Sprint Update: Progress Summary and Key Highlights

Dear Stakeholders,

As we progress through Sprint 2, I am pleased to provide you with an update on our current status, accomplishments, and any concerns.

Progress Summary:
We are currently focused on analyzing our current state and addressing data quality and system integration requirements.

Key Accomplishments (Done Tasks) - Sprint 2:
- T004 | Audit existing data infrastructure | STATUS: Done | Assignee: Priya Nair
- T005 | Map current logistics workflows | STATUS: Done | Assignee: James Wong

Work in Progress - Sprint 2:
- T006 | Identify data gaps and quality issues | STATUS: In Progress | Assignee: Priya Nair

Blockers/Concerns:
- T024 | Security review of AI infrastructure | STATUS: BLOCKED | Assignee: James Wong | Note: waiting for security team availability. This may impact our timeline if not addressed promptly.

Best regards,
Mira — Project Intelligence Assistant""",

}

# ── LLM Judge function ───────────────────────────────────────────────────────
def judge_output(test_case, mira_output):
    """Use GPT-4o-mini as LLM judge to score Mira's output."""
    
    prompt = f"""You are an expert evaluator for an AI Project Intelligence Assistant called Mira.

Evaluate the following AI output against the pass criteria and expected keywords.

TEST ID: {test_case['test_id']}
AGENT: {test_case['agent']}
USER REQUEST: {test_case['user_request']}
PASS CRITERIA: {test_case['pass_criteria']}
EXPECTED KEYWORDS: {', '.join(test_case['expected_keywords'])}
MUST NOT CONTAIN: {', '.join(test_case['must_not_contain']) if test_case['must_not_contain'] else 'None'}

MIRA'S OUTPUT:
{mira_output}

Evaluate on these 3 metrics (score each 0.0 to 1.0):
1. Groundedness: Is the output grounded in the actual project data? Does it reference real facts?
2. Completeness: Does it cover all expected keywords and meet the pass criteria?
3. Accuracy: Is the information correct? Does it avoid must-not-contain items?

Respond in this exact JSON format:
{{
  "groundedness": <score 0.0-1.0>,
  "completeness": <score 0.0-1.0>,
  "accuracy": <score 0.0-1.0>,
  "overall": <average of the 3 scores>,
  "verdict": "<PASS or FAIL>",
  "issues": "<brief description of any issues found, or 'None' if all good>"
}}"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )
    
    result_text = response.choices[0].message.content.strip()
    
    # Clean JSON if wrapped in markdown
    if result_text.startswith("```"):
        result_text = result_text.split("```")[1]
        if result_text.startswith("json"):
            result_text = result_text[4:]
    
    return json.loads(result_text)

# ── Run evaluation ───────────────────────────────────────────────────────────
def run_evaluation():
    print("\n" + "="*60)
    print("MIRA EVALUATION REPORT — LLM Judge (gpt-4o-mini)")
    print("="*60)
    
    results = []
    total_scores = []
    
    for test_case in ground_truth["tests"]:
        test_id = test_case["test_id"]
        mira_output = mira_outputs.get(test_id, "NO OUTPUT PROVIDED")
        
        print(f"\nEvaluating {test_id} — {test_case['agent']}...")
        
        scores = judge_output(test_case, mira_output)
        
        result = {
            "test_id": test_id,
            "agent": test_case["agent"],
            "scores": scores
        }
        results.append(result)
        total_scores.append(scores["overall"])
        
        # Print result
        verdict_icon = "✅" if scores["verdict"] == "PASS" else "❌"
        print(f"{verdict_icon} {test_id} | Groundedness: {scores['groundedness']:.2f} | "
              f"Completeness: {scores['completeness']:.2f} | "
              f"Accuracy: {scores['accuracy']:.2f} | "
              f"Overall: {scores['overall']:.2f} | {scores['verdict']}")
        if scores["issues"] != "None":
            print(f"   Issues: {scores['issues']}")
    
    # Summary
    avg_score = sum(total_scores) / len(total_scores)
    print("\n" + "="*60)
    print(f"OVERALL AVERAGE SCORE: {avg_score:.2f}")
    print(f"TESTS EVALUATED: {len(results)}")
    print("="*60)
    
    # Save results
    with open("results/eval_results.json", "w") as f:
        json.dump(results, f, indent=2)
    print("\nResults saved to results/eval_results.json")

if __name__ == "__main__":
    run_evaluation()