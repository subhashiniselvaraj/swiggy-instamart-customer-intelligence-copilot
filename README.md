# Swiggy Instamart Customer Intelligence Co-Pilot

## Overview

This academic capstone demonstrates a customer intelligence and support co-pilot for a fictional quick-commerce business using synthetic Instamart-style data.

The project combines data auditing, cleaning, SQLite analytics, customer segmentation, lapse prediction, privacy-aware support ticket triage, policy retrieval, and a bounded refund agent.

All customer records, policies, orders, and refunds are simulated. No real Swiggy customer information or payment systems are used. LLM behavior is simulated locally through `mock_llm.py`; no external LLM API or API key is required.

The instructor-aligned implementation is in `instructor_work/`. Required output artifacts are also provided in the repository-root `data/`, `sql/`, and `outputs/` directories.

## Reproduce

Use Python 3.11 or newer and SQLite 3.25 or newer. Run these commands from the repository root in a Windows PowerShell terminal.

1. Create a virtual environment:

   ```powershell
   python -m venv .venv
   ```

2. Activate it:

   ```powershell
   .\.venv\Scripts\Activate.ps1
   ```

3. Install the permitted dependencies:

   ```powershell
   python -m pip install -r requirements.txt
   ```

4. Enter the instructor-aligned implementation:

   ```powershell
   cd instructor_work
   ```

5. Generate the deterministic synthetic source data and policy files:

   ```powershell
   python generate_data.py
   ```

6. Run the main pipeline:

   ```powershell
   python run_project.py
   ```

7. Generate the 6,000-token ticket-triage budget demonstration:

   ```powershell
   python -c "from src.triage import run_pipeline; run_pipeline(token_budget=6000)"
   ```

8. Run the seven refund-agent behavior scenarios and save their traces:

   ```powershell
   python -c "import json; from pathlib import Path; from src.refund_agent import run_agent; cases=[('S1','Please refund order ORD-100048'),('S2','Please refund order ORD-100067'),('S3','Please refund order ORD-100145'),('S4','Please refund order ORD-100001'),('S5','Please refund order ORD-100020'),('S6','Please refund order ORD-999999'),('S7','[LOOP] Please refund order ORD-100048')]; p=Path('outputs/agent_runs.jsonl'); p.parent.mkdir(exist_ok=True); f=p.open('w',encoding='utf-8'); [(lambda r: f.write(json.dumps(dict(scenario_id=s,user_message=m,**r))+'\n'))(run_agent(m,scenario_id=s)) for s,m in cases]; f.close(); print('Saved:',p)"
   ```

9. Return to the repository root:

   ```powershell
   cd ..
   ```

10. Copy the instructor-aligned output artifacts to the required root locations:

   ```powershell
   New-Item -ItemType Directory -Force data\clean,sql,outputs,state | Out-Null
   Copy-Item instructor_work\data\clean\customers.csv,instructor_work\data\clean\products.csv,instructor_work\data\clean\orders.csv -Destination data\clean\
   Copy-Item instructor_work\data\instamart.db -Destination data\
   Copy-Item instructor_work\sql\queries.sql -Destination sql\
   Copy-Item instructor_work\outputs\customer_segments.csv,instructor_work\outputs\lapse_model.joblib,instructor_work\outputs\retention_list.csv,instructor_work\outputs\triage_results.csv,instructor_work\outputs\triage_budget_demo.csv,instructor_work\outputs\agent_runs.jsonl,instructor_work\outputs\refund_ledger.jsonl -Destination outputs\
   Copy-Item instructor_work\state\*.json -Destination state\ -ErrorAction SilentlyContinue
   ```

The root also contains an earlier prototype. The reproducible instructor-aligned pipeline is `instructor_work/run_project.py`, not the root-level `run_project.py`.

## Part A

**Data engineering, auditing, cleaning, and SQL analytics**

The data pipeline audits synthetic customer, product, and order records; handles duplicate records, missing values, inconsistent categories, and invalid numeric fields; and loads cleaned data into SQLite.

The generated dataset includes approximately 1,200 customers. The cleaned order dataset contains 12,309 distinct orders, including 11,110 completed and 1,199 cancelled orders.

Completed-order revenue is approximately INR 2,998,668.80.

The implementation includes seven SQL analysis queries in `sql/queries.sql`, together with data validation and analytical summaries. The pipeline reports successful validation checkpoints when its assertions pass.

**Key files:** `instructor_work/src/data_pipeline.py`, `data/clean/`, `data/instamart.db`, and `sql/queries.sql`.

## Part B

**Customer segmentation and lapse prediction**

Customer segmentation uses recency, frequency, and monetary features, K-Means clustering, silhouette analysis, and PCA.

The analysis covers 1,175 customers with purchasing activity. The strongest recorded silhouette score is approximately **0.5255** at **four clusters**.

Lapse prediction uses supervised classification to identify customers at risk of becoming inactive. Recorded test F1 scores are approximately:

| Model | Test F1 |
|---|---:|
| Logistic Regression | 0.6480 |
| Random Forest | 0.6369 |

The saved model is `outputs/lapse_model.joblib`. Customer segmentation and retention outputs are available in `outputs/customer_segments.csv` and `outputs/retention_list.csv`.

These scores describe performance on synthetic data, not real-world predictive performance.

## Part C

**Privacy-aware support ticket triage**

The triage pipeline uses the local mock LLM to classify support tickets into billing, delivery, technical, and fraud categories.

It includes personally identifiable information redaction, retry handling, structured JSON parsing, keyword fallback, invalid-output handling, and priority-based routing.

The full dataset contains **164 support tickets**. The implementation routes fraud cases to the security team, prioritizes premium customers, and sends unsuitable or unresolved cases for human review.

The 6,000-token budget demonstration produced the following statuses:

| Status | Tickets |
|---|---:|
| Budget exhausted | 81 |
| Classified using JSON | 66 |
| Classified using keywords | 5 |
| Skipped empty | 4 |
| Flagged long | 4 |
| Flagged invalid output | 4 |

The main outputs are `outputs/triage_results.csv` and `outputs/triage_budget_demo.csv`.

## Part D

**Policy retrieval and bounded refund agent**

The policy retrieval system uses TF-IDF matching to search synthetic policy documents and return relevant policy evidence. The evaluation includes 14 questions: 12 policy-related questions and two unrelated-question fallback cases.

The refund agent uses database-backed tools for order lookup, policy search, refund calculation, simulated refund issuance, and human escalation.

The agent limits model calls, token usage, and execution time. It records tool activity and supports checkpoint-based recovery following a simulated crash.

The following seven behavior scenarios were tested using orders selected from the generated database. They reproduce the expected refund-rule outcomes; they are **not claimed to be the instructor's original scenario CSV**.

| Scenario | Test order | Verified result | Model calls |
|---|---|---|---:|
| S1 | ORD-100048 | REFUND INR 128.25 | 5 |
| S2 | ORD-100067 | REFUND INR 135.00 | 5 |
| S3 | ORD-100145 | ESCALATE refund above INR 1,000 | 5 |
| S4 | ORD-100001 | DENIED: delivered within 45 minutes | 4 |
| S5 | ORD-100020 | DENIED: cancelled order | 3 |
| S6 | ORD-999999 | NOT_FOUND | 2 |
| S7 | ORD-100048 with loop trigger | FALLBACK_MAX_ITERATIONS | 6 |

Additional safety checks were executed:

- **Crash and resume:** Simulated a crash after two tools. Resumption completed the refund using `get_order`, `search_policy`, `calculate_refund`, and `issue_refund`, with five total model calls and without replaying the first two tools.
- **Token limit:** A 200-token limit produced `FALLBACK_TOKEN_LIMIT`.
- **Timeout:** A zero-second time limit produced `FALLBACK_TIMEOUT` before any model call.
- **Iteration limit:** The loop scenario produced `FALLBACK_MAX_ITERATIONS` after six calls.

The agent follows a bounded ReAct-style tool-use cycle, selecting and observing tools incrementally. Unlike a fixed plan-and-execute workflow, its next action depends on the previous observation, with explicit safety limits and human fallback.

Saved evidence is in `outputs/agent_runs.jsonl`, `outputs/refund_ledger.jsonl`, and the `state/` checkpoint directory. Refund issuance is simulated through ledger entries; no real money is transferred.

## Limitations and Next Steps

This is an educational prototype built on synthetic data and simulated LLM responses. Results should not be interpreted as operational performance on real Swiggy customers.

The repository retains an older prototype alongside the instructor-aligned implementation. The primary reproduction workflow therefore runs from `instructor_work/` and copies the resulting artifacts into the required repository-root directories.

The original instructor scenario CSV was not available in the local materials used for these tests, so equivalent scenarios were constructed from actual generated orders. These tests validate refund behavior but do not establish equivalence to the missing official scenario file.

Further work would include independent verification against the instructor's original supplied files, additional model-leakage checks, automated end-to-end tests from a clean clone, stronger refund-ledger idempotency, and production-grade monitoring and access controls.