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

# ── Load Mira outputs (updated with Phase 5 re-run outputs) ──────────────────
mira_outputs = {
    "T1": """Project Plan for AI Adoption Project at ABCDE Ltd.

Phase 1: Project Initiation - Week Range: Weeks 1-2
Key Activities: Define project scope and objectives. Form cross-functional task force. Conduct initial stakeholder alignment meeting.
Milestone/Deliverable: Project charter signed off; Team structure finalized.

Phase 2: Current State Analysis - Week Range: Weeks 3-4
Key Activities: Audit existing data infrastructure. Map current logistics workflows. Identify data gaps and quality issues.
Milestone/Deliverable: Current systems audit report; Gap analysis report.

Phase 3: Use Case Selection - Week Range: Weeks 5-6
Key Activities: Shortlist AI use cases. Define success criteria for each use case. Conduct vendor evaluation for ML platform.
Milestone/Deliverable: Final list of prioritized use cases with success criteria.

Phase 4: Pilot Design - Week Range: Weeks 7-10
Key Activities: Collect historical demand data. Develop data cleaning and preprocessing pipeline. Design demand forecasting and route optimization models. Build model training pipeline.
Milestone/Deliverable: Working prototype models; Data pipelines established.

Phase 5: Pilot Implementation - Week Range: Weeks 11-14
Key Activities: Deploy demand model to test environment. Run pilot with logistics team. Collect pilot feedback and metrics.
Milestone/Deliverable: Pilot results report; User feedback and performance metrics.

Phase 6: Evaluation and Iteration - Week Range: Weeks 15-16
Key Activities: Iterate on model based on feedback.
Milestone/Deliverable: Updated models and process refinements.

Phase 7: Full Deployment - Week Range: Weeks 17-22
Key Activities: Prepare production deployment plan. Implement staff training program. Full production rollout.
Milestone/Deliverable: Full production rollout; Training sessions completed.

Phase 8: Monitoring and Review - Week Range: Weeks 23-24
Key Activities: Set up continuous monitoring. Prepare project closure report.
Milestone/Deliverable: Project closure report; Recommendations for future scaling.""",

    "T2": """INSUFFICIENT INFORMATION: I need more detail to create a grounded plan. Please provide the following:

1. Project scope (specific functionalities and goals for the chatbot).
2. Timeline or duration for the project.
3. Any phases or milestones you have in mind.
4. Team members involved or required resources.
5. Any specific challenges or risks you foresee.""",

    "T3": """Risk Assessment for AI Adoption Project at ABCDE Ltd.

| Category | Risk Description | Impact | Mitigation |
|----------|-----------------|--------|------------|
| Data Quality and Availability | Incomplete or unstructured data. | Poor model performance. | Early data audits and data governance. |
| Integration Issues | Difficulty integrating AI with legacy systems. | Deployment delays. | Integration roadmap, APIs/middleware. |
| Talent and Skills Gap | Lack of internal AI/ML expertise. | Vendor overreliance, slow progress. | Staff training, hire specialists. |
| Change Resistance | Employees resist AI workflows. | Low adoption, reduced ROI. | Change management, early engagement. |
| Ethical and Legal Concerns | Biased models or data privacy violations. | Legal and reputational damage. | Involve legal early, fairness checks. |
| Cost Overruns | Underestimation of AI costs. | Budget constraints, delays. | Realistic budget, contingency funds. |
| Unrealistic Expectations | Stakeholders expect immediate ROI. | Disillusionment, loss of support. | Align expectations, show quick wins. |
| Model Performance Drift | Models lose accuracy over time. | Incorrect decisions, trust erosion. | Regular retraining, monitoring dashboards. |
| Security Vulnerabilities | Models targeted by adversarial attacks. | Data breaches. | AI security best practices, penetration testing. |
| Vendor Lock-in | Overdependence on one platform. | Flexibility loss, switching costs. | Open standards, flexible vendor terms. |""",

    "T4": """INSUFFICIENT INFORMATION: I need more detail to assess risks. Please provide the following:

1. Project description or scope.
2. Specific goals or objectives of the project.
3. Timeline or phases of the project.
4. Any known risks or concerns already identified.""",

    "T5": """Sprint 3 Status Report

Tasks Overview:
1. Task T007 | STATUS: In Progress
2. Task T008 | STATUS: To Do
3. Task T009 | STATUS: To Do
4. Task T025 | STATUS: In Progress

Grouped by Status:

In Progress (2)
- Task T007 | STATUS: In Progress
- Task T025 | STATUS: In Progress

To Do (2)
- Task T008 | STATUS: To Do
- Task T009 | STATUS: To Do

BLOCKERS
- Task T024 | STATUS: BLOCKED | Assignee: James Wong | Note: waiting for security team availability""",

    "T6": """INSUFFICIENT INFORMATION: I need task data to generate a status report.""",

    "T7": """Based on the risk data provided, the top 3 risks for the ABCDE Ltd project are as follows:

1. R01 [Data Quality and Availability]
   - Category: Data Management
   - Description: Incomplete or unstructured data.
   - Impact: Poor model performance.
   - Mitigation: Early data audits and data governance.
   - Justification: Data quality is fundamental to the success of AI models.

2. R02 [Integration Issues]
   - Category: Technical Integration
   - Description: Difficulty integrating AI with legacy systems.
   - Impact: Deployment delays.
   - Mitigation: Integration roadmap, APIs/middleware.
   - Justification: Integration difficulties can halt progress, impacting timelines and costs.

3. R03 [Talent and Skills Gap]
   - Category: Human Resources
   - Description: Lack of internal AI/ML expertise.
   - Impact: Vendor overreliance, slow progress.
   - Mitigation: Staff training, hire specialists.
   - Justification: A skills gap can slow down project implementation.""",

    "T8": """Based on the task board, the following tasks are blocked or at risk of missing their deadline:

Blocked Tasks:
1. Task T024: Security review of AI infrastructure
   - Status: BLOCKED
   - Assignee: James Wong
   - Note: Waiting for security team availability.

Tasks at Risk of Missing Their Deadline:
1. Task T006: Identify data gaps and quality issues
   - Status: In Progress
   - Assignee: Priya Nair
   - Potential Delay: If data issues are not resolved promptly, subsequent phases may be impacted.

2. Task T025: Legal review of data usage
   - Status: In Progress
   - Assignee: Sarah Lin
   - Potential Delay: Legal review may encounter delays, affecting compliance and ethical considerations.""",

    "T9": """INSUFFICIENT INFORMATION: I need more detail to create a grounded plan. Please provide the following:

1. Project description or goal
2. Project scope or focus areas
3. Specific tasks or activities to be included
4. Key milestones or deliverables
5. Team members involved or any relevant resources

With this information, I can help generate a structured project plan.""",

    "T10": """Current Project Status:

- Done: 5
- In Progress: 3
- To Do: 16
- Blocked: 1

Total Tasks: 25""",

    "T11": """The upcoming milestones in the next 2 weeks based on the project timeline are:

Phase 2 - Current State Analysis (weeks 3-4):
- Current systems audit report
- Gap analysis report

Phase 3 - Use Case Selection (weeks 5-6):
- Final list of prioritized use cases with success criteria

These milestones are the next in line as the project progresses.""",

    "T12": """Subject: Sprint 2 Progress Update

Dear Stakeholders,

I hope this message finds you well. Below is the progress update for Sprint 2 of our project at ABCDE Ltd.

Progress Summary:
We are currently focusing on assessing our existing processes and systems, aimed at identifying data sources and gaps. Significant strides have been made in mapping our current logistics workflows.

Key Accomplishments (Done tasks):
- Audit existing data infrastructure - Completed by Priya Nair
- Map current logistics workflows - Completed by James Wong

Work in Progress:
- Identify data gaps and quality issues - In progress by Priya Nair

Blockers/Concerns:
It is important to note that the task Security review of AI infrastructure (T024) is currently blocked, awaiting availability from the security team, which may impact our timelines.

Thank you for your continued support and engagement. We will keep you updated on our progress as we move forward.

Best regards,

Mira - Project Intelligence Assistant""",
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
