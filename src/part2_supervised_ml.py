from pathlib import Path
import json
import warnings
import pandas as pd
import numpy as np
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV, StratifiedKFold
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, classification_report
import joblib

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "processed" / "online_retail_clean.csv"
OUT = ROOT / "outputs"
MODEL_DIR = ROOT / "outputs"

def main():
    if not DATA.exists():
        raise FileNotFoundError("Run Part 1 first: python -m src.part1_eda")
    OUT.mkdir(parents=True, exist_ok=True)
    df = pd.read_csv(DATA, parse_dates=["InvoiceDate"])
    df = df.sort_values("InvoiceDate")
    max_date = df["InvoiceDate"].max()
    cutoff = max_date - pd.Timedelta(days=90)
    feature_data = df[df["InvoiceDate"] <= cutoff].copy()
    future_data = df[(df["InvoiceDate"] > cutoff) & (df["InvoiceDate"] <= max_date)].copy()

    if feature_data.empty or future_data.empty:
        raise ValueError("Not enough data before/after temporal cutoff to create a future-purchase target.")

    # Customer-level features use only the pre-cutoff period.
    customer = feature_data.groupby("CustomerID").agg(
        recency_days=("InvoiceDate", lambda x: int((cutoff - x.max()).days)),
        invoice_count=("InvoiceNo", "nunique"),
        quantity_sum=("Quantity", "sum"),
        sales_sum=("Sales", "sum"),
        product_count=("StockCode", "nunique"),
        country=("Country", lambda x: x.mode().iat[0] if not x.mode().empty else "Unknown")
    ).reset_index()

    future_buyers = set(future_data["CustomerID"].unique())
    customer["repeat_purchase_90d"] = customer["CustomerID"].isin(future_buyers).astype(int)
    y = customer["repeat_purchase_90d"]
    X = customer[["recency_days", "invoice_count", "quantity_sum", "sales_sum", "product_count", "country"]]

    # Chronological feature cutoff avoids using future purchases as features.
    # Hold out customers for evaluation; report the limitations of this customer-level design.
    from sklearn.model_selection import train_test_split
    if y.nunique() < 2 or y.value_counts().min() < 3:
        raise ValueError(
            "The target has too few examples of one class for a reliable split. "
            "Inspect outputs/part1_summary.json and adjust the prediction window/cutoff with explanation."
        )
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=42, stratify=y
    )
    numeric = ["recency_days", "invoice_count", "quantity_sum", "sales_sum", "product_count"]
    categorical = ["country"]
    numeric_pipe = Pipeline([("imputer", SimpleImputer(strategy="median")), ("scale", StandardScaler())])
    categorical_pipe = Pipeline([("imputer", SimpleImputer(strategy="most_frequent")),
                                 ("onehot", OneHotEncoder(handle_unknown="ignore"))])
    prep = ColumnTransformer([("num", numeric_pipe, numeric), ("cat", categorical_pipe, categorical)])

    candidates = {
        "logistic_regression": Pipeline([("prep", prep), ("model", LogisticRegression(max_iter=2000, class_weight="balanced"))]),
        "random_forest": Pipeline([("prep", prep), ("model", RandomForestClassifier(random_state=42, class_weight="balanced"))])
    }
    results = {}
    best_name, best_pipe, best_f1 = None, None, -1
    for name, pipe in candidates.items():
        pipe.fit(X_train, y_train)
        pred = pipe.predict(X_test)
        probs = pipe.predict_proba(X_test)[:, 1]
        metrics = {
            "accuracy": float(accuracy_score(y_test, pred)),
            "precision": float(precision_score(y_test, pred, zero_division=0)),
            "recall": float(recall_score(y_test, pred, zero_division=0)),
            "f1": float(f1_score(y_test, pred, zero_division=0)),
            "roc_auc": float(roc_auc_score(y_test, probs)) if y_test.nunique() == 2 else None
        }
        results[name] = metrics
        if metrics["f1"] > best_f1:
            best_name, best_pipe, best_f1 = name, pipe, metrics["f1"]

    # Tune the best candidate using training data only; test set remains held out.
    if best_name == "logistic_regression":
        grid = {"model__C": [0.1, 1.0, 10.0]}
    else:
        grid = {"model__n_estimators": [100, 200], "model__max_depth": [None, 8, 16]}
    cv = StratifiedKFold(n_splits=3, shuffle=True, random_state=42)
    search = GridSearchCV(best_pipe, grid, scoring="f1", cv=cv, n_jobs=-1)
    search.fit(X_train, y_train)
    tuned = search.best_estimator_
    pred = tuned.predict(X_test)
    probs = tuned.predict_proba(X_test)[:, 1]
    tuned_metrics = {
        "accuracy": float(accuracy_score(y_test, pred)),
        "precision": float(precision_score(y_test, pred, zero_division=0)),
        "recall": float(recall_score(y_test, pred, zero_division=0)),
        "f1": float(f1_score(y_test, pred, zero_division=0)),
        "roc_auc": float(roc_auc_score(y_test, probs)),
        "classification_report": classification_report(y_test, pred, output_dict=True, zero_division=0)
    }
    payload = {
        "target": "customer made at least one purchase in the final 90-day window after the feature cutoff",
        "feature_cutoff": str(cutoff),
        "dataset_max_date": str(max_date),
        "feature_customer_count": int(len(customer)),
        "positive_rate": float(y.mean()),
        "candidate_test_metrics": results,
        "selected_model": best_name,
        "tuned_best_params": search.best_params_,
        "tuned_test_metrics": tuned_metrics,
        "caution": "Educational temporal target. The test split is customer-level; further temporal backtesting is recommended for production."
    }
    (OUT / "part2_metrics.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")
    joblib.dump(tuned, OUT / "repeat_purchase_model.joblib")
    print(json.dumps(payload, indent=2))
    print(f"\nSaved metrics to {OUT / 'part2_metrics.json'}")

if __name__ == "__main__":
    main()
