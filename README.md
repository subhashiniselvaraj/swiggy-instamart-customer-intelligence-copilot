# Swiggy Instamart Customer Intelligence Co-Pilot

## Project Overview
An educational end-to-end customer intelligence and support co-pilot built using **synthetic quick-commerce data**. The project combines data engineering, SQL analytics, machine learning, simulated LLM ticket triage, policy retrieval, and a rule-based refund agent.

**Note:** No real Swiggy customer data, official policies, payments, or refunds are used.

## Capstone Implementation — Parts A–D

| Part | Implementation | Key Results |
|---|---|---|
| **A — Data Engineering & SQL** | Data auditing, cleaning, validation, SQLite storage, and SQL analytics | All validation checkpoints passed; 7 SQL queries executed |
| **B — Customer Intelligence** | RFM segmentation, K-Means clustering, and lapse prediction | 1,175 customers; best silhouette **0.5255** (4 clusters); Logistic Regression F1 **0.6480**, Random Forest F1 **0.6369** |
| **C — Support Ticket Triage** | Mock LLM, structured JSON validation, PII redaction, retries, fallback, and routing | 164 tickets processed; 135 structured classifications; 12 keyword fallbacks |
| **D — Policy RAG & Refund Agent** | TF-IDF policy retrieval, unrelated-question fallback, and simulated refund decisions | 14 retrieval evaluations; 12 policy-related matches and 2 fallbacks; refund, denial, and escalation scenarios tested |

## Run the Project

Install dependencies from the repository root:

```bash
python -m pip install -r requirements.txt
```

Run the instructor-aligned implementation:

```bash
cd instructor_work
python run_project.py
```

The project uses a **local simulated LLM** and requires no paid API key.

## Key Files

- `instructor_work/run_project.py` — Main capstone pipeline
- `instructor_work/src/` — Modular Parts A–D implementation
- `instructor_work/sql/queries.sql` — Seven SQL queries
- `instructor_work/notebooks/Customer_Intelligence_Support_Copilot.ipynb` — Executed Jupyter notebook
- `instructor_work/outputs/` — Saved segmentation, prediction, and model artifacts
- `outputs/figures/` — Visualizations
- `run_project.py` — Additional original prototype

## Validation and Improvements

The instructor-aligned pipeline completed successfully, the notebook sections were executed, and the original automated test suite passed **7 tests**.

Additional functionality includes privacy-aware ticket triage, structured-output validation and fallback, policy-based refund escalation, and an original prototype with separate retail analysis. These demonstrate extensions beyond the core customer segmentation workflow.

**Limitations:** Results are based on synthetic data. Model preprocessing requires further leakage review, the LLM is simulated, and the refund agent does not perform real financial transactions. This is an academic demonstration, not a production system.