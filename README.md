# Swiggy Instamart Customer Intelligence Co-Pilot

## Project Overview

An educational customer intelligence and support co-pilot for a fictional Instamart-style quick-commerce business.

The project combines data engineering, SQL analytics, customer segmentation, lapse prediction, support ticket triage, policy retrieval, and a simulated refund decision workflow.

**Data disclaimer:** All Instamart-style customer, order, product, ticket, and policy data in this project is synthetic. It does not contain real Swiggy customer information or official Swiggy policies. No real refunds or payments are processed.

The repository contains two complementary implementations:

1. **Instructor-aligned capstone (`instructor_work/`)** — Covers Parts A–D of the Customer Intelligence & Support Copilot teaching kit.
2. **Original prototype (repository root)** — Demonstrates customer segmentation, supervised ticket classification, policy retrieval, and additional retail analysis.

## Project Objectives

- Audit, clean, validate, and store synthetic quick-commerce data in SQLite.
- Answer business questions using SQL joins, aggregations, subqueries, CTEs, and window functions.
- Segment customers using Recency, Frequency, and Monetary (RFM) features.
- Compare K-Means clustering options using silhouette scores.
- Train and evaluate customer lapse prediction models.
- Triage support tickets using a simulated LLM, structured output validation, retries, and privacy redaction.
- Retrieve relevant policy passages using TF-IDF similarity.
- Demonstrate policy-based refund eligibility, human escalation, and a simulated refund ledger.
- Provide a reproducible notebook and inspectable outputs.

## Repository Structure

```text
swiggy-instamart-customer-intelligence-copilot/
├── README.md
├── requirements.txt
├── run_project.py                    # Original prototype runner
├── generate_data.py                  # Original prototype data generator
├── customer_segmentation.py
├── triage.py
├── policy_rag.py
├── src/                              # Original prototype and retail analysis
├── data/
├── outputs/
├── tests/
├── generate_data_original.py         # Backup of original generator
└── instructor_work/
    ├── generate_data.py
    ├── mock_llm.py
    ├── run_project.py                # Instructor-aligned Parts A–D runner
    ├── src/
    │   ├── data_pipeline.py
    │   ├── customer_models.py
    │   ├── triage.py
    │   ├── policy_rag.py
    │   └── refund_agent.py
    ├── sql/
    │   └── queries.sql
    ├── notebooks/
    │   └── Customer_Intelligence_Support_Copilot.ipynb
    ├── data/
    │   ├── raw/
    │   ├── clean/
    │   ├── policies/
    │   └── instamart.db
    ├── outputs/
    └── state/
```

Some output and state directories are created when the relevant workflows run.

## Requirements

- Python 3.10 or newer
- pip
- Dependencies listed in `requirements.txt`

Install dependencies from the repository root:

```bash
python -m pip install -r requirements.txt
```

The instructor-aligned workflow uses a local mock LLM and does not require a paid LLM API key.

## Running the Instructor-Aligned Capstone

From the repository root:

```bash
cd instructor_work
python run_project.py
```

This runs the main stages for Parts A–D using the synthetic data included in the instructor workspace.

For a fresh data generation run, from inside `instructor_work`:

```bash
python generate_data.py
python run_project.py
```

**Note:** The data generator must be configured to write to `data/raw` and `data/policies` relative to `instructor_work` when launched from that directory.

The main instructor runner covers data preparation, segmentation, lapse modeling, ticket triage, and policy retrieval. The refund agent is tested separately.

## Part A — Data Engineering and SQL

The instructor-aligned data pipeline audits and cleans synthetic customer, product, and order records.

It handles issues including:

- Duplicate records
- Missing and invalid values
- Inconsistent categorical values
- Invalid order amounts and delivery durations
- Order and customer data validation

Cleaned data is stored in CSV files and in `instructor_work/data/instamart.db`.

The seven SQL queries in `instructor_work/sql/queries.sql` demonstrate filtering, aggregation, joins, subqueries, CTEs, ranking, and running totals.

**Verified result:** All data validation checkpoints passed, and all seven SQL queries executed successfully.

## Part B — Customer Intelligence

### RFM Segmentation

Customers are characterized using:

- **Recency:** How recently a customer placed an order.
- **Frequency:** How frequently a customer placed orders.
- **Monetary:** How much a customer spent.

K-Means clustering is evaluated for `k = 2` through `k = 8`.

**Verified results:**

| Metric | Result |
|---|---:|
| Customers segmented | 1,175 |
| Best silhouette score | 0.5255 |
| Cluster count with best silhouette | 4 |

The workflow also produces segment profiles and PCA-based diagnostics.

### Customer Lapse Prediction

A supervised learning workflow predicts customer lapse using historical customer behavior.

The workflow compares Logistic Regression and Random Forest, uses hyperparameter search, and reports precision, recall, F1-score, and confusion matrices.

**Verified held-out test results:**

| Model | Precision | Recall | F1-score |
|---|---:|---:|---:|
| Logistic Regression | 0.6444 | 0.6517 | 0.6480 |
| Random Forest | 0.6333 | 0.6404 | 0.6369 |

The modeling cohort contains 1,156 customers, of whom 443 have a positive lapse label.

The saved model and retention candidate list are educational demonstrations. The current implementation should not be considered production-ready; preprocessing and leakage controls require further review before real-world use.

## Part C — Support Ticket Triage

The instructor-aligned ticket triage pipeline uses a **simulated LLM**, not a live hosted language model.

It demonstrates:

- Redaction of email addresses, phone numbers, and order identifiers
- Structured JSON classification with an allowlisted category set
- Retry handling for simulated transient errors
- Keyword fallback and invalid-output handling
- Ticket priority and routing decisions
- Token budget tracking and human review pathways

**Verified results:**

| Metric | Result |
|---|---:|
| Tickets processed | 164 |
| Structured JSON classifications | 135 |
| Keyword fallback classifications | 12 |
| Invalid outputs flagged | 9 |
| Long tickets flagged | 4 |
| Empty tickets skipped | 4 |
| Simulated tokens used | 12,520 |

The pipeline recorded 55 email redactions, 91 phone redactions, and 132 order identifier redactions.

These are workflow execution results, not a measured classification accuracy score.

## Part D — Policy Retrieval and Refund Agent

### Policy Retrieval

The instructor-aligned Policy RAG component uses policy text chunking and TF-IDF similarity to retrieve relevant passages.

**Verified results:**

- 15 indexed policy chunks
- 14 evaluation questions
- 12 policy-related questions with the expected policy facts found
- 2 unrelated questions correctly handled with fallback

This is a retrieval-based demonstration. It does not establish the reliability of a production generative RAG system.

### Simulated Refund Agent

The refund agent uses synthetic order records and sample policy rules to demonstrate a bounded decision workflow.

The example policy allows a full refund for a completed order delivered more than 45 minutes late. Refunds above INR 1,000 require human escalation.

**Separately tested scenarios:**

| Scenario | Observed result |
|---|---|
| Completed order, 20-minute delivery | DENIED |
| Completed order, 65-minute delivery, INR 128.25 | REFUND |
| Completed order, 54-minute delivery, INR 1,999 | ESCALATE |

The agent writes simulated actions to a local ledger. **No real money moves.** The implementation is not authorized or sufficiently hardened for real financial decisions.

## Jupyter Notebook

The instructor notebook is located at:

`instructor_work/notebooks/Customer_Intelligence_Support_Copilot.ipynb`

The notebook file has been verified as readable and contains 25 cells, including 11 code cells.

**Validation status:** The notebook has not yet been confirmed to execute successfully from top to bottom.

## Original Prototype

The repository root also contains an earlier working demonstration.

From the repository root:

```bash
python run_project.py
```

The original runner demonstrates:

1. Synthetic data generation
2. Customer segmentation
3. Support ticket classification using TF-IDF and Logistic Regression
4. Policy retrieval and human escalation examples

Its ticket classification data is highly standardized, so high performance on those synthetic examples should not be interpreted as expected real-world performance.

The original prototype also includes additional analysis using the **UCI Online Retail dataset**, which represents a different retail business and is not Swiggy Instamart data.

## Tests and Validation

The following checks have been completed:

- Original project runner executed successfully
- Original automated test suite: **7 tests passed**
- Instructor data pipeline: **all validation checkpoints passed**
- Instructor SQL: **7 of 7 queries executed successfully**
- Instructor segmentation and lapse models: **executed successfully**
- Instructor triage: **164 tickets processed**
- Instructor policy retrieval: **14 evaluation questions executed**
- Refund agent: **three representative scenarios tested**
- Instructor main runner: **completed successfully**

The original seven automated tests cover the original guardrails; they are not comprehensive tests of every instructor-aligned component.

## Limitations

- All Instamart-style data and policies are synthetic and illustrative.
- No real Swiggy systems or customer accounts are accessed.
- The mock LLM does not measure the quality of a real hosted language model.
- Synthetic data performance may not generalize to real customers.
- Model preprocessing and data leakage controls require further review.
- Policy retrieval can fail on ambiguous or unfamiliar questions.
- The refund agent requires stronger independent eligibility, authorization, and duplicate-action safeguards before any production use.
- Human review is required for uncertain, disputed, high-value, or sensitive cases.

## Responsible Use

This repository is an educational capstone only. Do not use it to make real refund, payment, fraud, account, or customer eligibility decisions. All financial actions are simulated, and sensitive cases should be reviewed by authorized personnel.

## Author

Academic capstone project — **Swiggy Instamart Customer Intelligence Co-Pilot**.
