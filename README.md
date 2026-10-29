
# Swiggy Instamart Customer Intelligence Co-Pilot

## Project Overview

This project demonstrates a customer intelligence and support co-pilot for an Instamart-style quick-commerce business.

It combines customer segmentation, support ticket classification, and policy retrieval to demonstrate how data analytics and machine learning can support customer service operations.

**Data note:** The Instamart-style datasets in this project are synthetically generated for educational purposes. They are not real Swiggy customer records or official Swiggy policies. A separate exploratory analysis and repeat-purchase prediction component uses the UCI Online Retail dataset, which represents a different retail business.

## Project Objectives

- Generate and prepare sample customer, order, ticket, and policy datasets.
- Segment customers using Recency, Frequency, and Monetary (RFM) features.
- Compare K-Means clustering options using silhouette scores.
- Visualize customer segments using Principal Component Analysis (PCA).
- Classify support tickets using TF-IDF and Logistic Regression.
- Retrieve relevant sample policies for customer questions.
- Identify cases that should be referred to human support.
- Save results and evaluation metrics for inspection.

## Project Structure

```text
retail_customer_intelligence_capstone/
├── generate_data.py
├── customer_segmentation.py
├── triage.py
├── policy_rag.py
├── run_project.py
├── requirements.txt
├── README.md
├── data/
│   ├── raw/
│   └── processed/
├── outputs/
│   └── figures/
├── src/
└── tests/
```

## Requirements

- Python 3.10 or newer recommended
- pip
- The packages listed in `requirements.txt`

## Setup

Open a terminal in the project root and install dependencies:

```bash
python -m pip install -r requirements.txt
```

## Run the Project

Run all four Instamart-style demonstration components:

```bash
python run_project.py
```

The runner executes:

1. `generate_data.py`
2. `customer_segmentation.py`
3. `triage.py`
4. `policy_rag.py`

## Components

### 1. Synthetic Data Generation

Generates sample datasets for customers, orders, tickets, and illustrative policies.

Output files:
- `data/raw/customers.csv`
- `data/raw/orders.csv`
- `data/raw/tickets.csv`
- `data/raw/policies.csv`

### 2. Customer Segmentation

Calculates customer RFM features, compares K-Means cluster counts using silhouette scores, and creates a PCA visualization.

Output files:
- `outputs/customer_rfm_segments.csv`
- `outputs/customer_segment_summary.csv`
- `outputs/customer_segmentation_metrics.json`
- `outputs/figures/customer_segments_pca.png`

### 3. Support Ticket Triage

Uses TF-IDF text features and Logistic Regression to predict a ticket category and recommend a support team and priority.

Output files:
- `outputs/triaged_tickets.csv`
- `outputs/triage_metrics.json`

The generated ticket descriptions are highly standardized, so the evaluation score should not be interpreted as expected performance on real customer complaints.

### 4. Policy Retrieval Demonstration

Uses TF-IDF similarity to retrieve sample policy text relevant to customer questions.

Output file:
- `outputs/policy_rag_demo.json`

This is a retrieval demonstration, not a full generative RAG system. The policies are illustrative, and retrieved results should be checked before being used for customer decisions.

## Additional Retail Analysis

The repository also includes a separate UCI Online Retail analysis and repeat-purchase prediction workflow in `src/`. This dataset is not Swiggy Instamart data and should be interpreted separately from the synthetic quick-commerce demonstration.

## Limitations

- All Instamart-style data is synthetic.
- The sample policies are not official Swiggy policies.
- Model performance on synthetic data may not generalize to real customers.
- Policy retrieval uses text similarity and can return irrelevant matches.
- Human review is needed for uncertain, disputed, or sensitive customer issues.

## Responsible Use

Do not use this demonstration to make real refund, payment, or customer account decisions. Verify order and payment records and refer uncertain cases to an authorized human support agent.

## Author

Add your name and project details here before submission.
