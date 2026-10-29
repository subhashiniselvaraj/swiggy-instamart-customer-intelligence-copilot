
from pathlib import Path
import json

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report, accuracy_score


ROOT = Path(__file__).resolve().parent
DATA_FILE = ROOT / "data" / "raw" / "tickets.csv"
OUTPUT_DIR = ROOT / "outputs"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def main():
    tickets = pd.read_csv(DATA_FILE)
    tickets = tickets.dropna(subset=["description", "ticket_type"]).copy()

    X = tickets["description"].astype(str)
    y = tickets["ticket_type"].astype(str)

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.25,
        random_state=42,
        stratify=y,
    )

    model = Pipeline([
        ("tfidf", TfidfVectorizer(ngram_range=(1, 2))),
        ("classifier", LogisticRegression(max_iter=1000)),
    ])

    model.fit(X_train, y_train)
    predictions = model.predict(X_test)

    accuracy = accuracy_score(y_test, predictions)
    report = classification_report(
        y_test, predictions, output_dict=True, zero_division=0
    )

    tickets["predicted_ticket_type"] = model.predict(
        tickets["description"].astype(str)
    )

    tickets["recommended_team"] = tickets["predicted_ticket_type"].map({
        "Delayed order": "Delivery Support",
        "Payment issue": "Payments Support",
        "Product quality": "Quality Support",
        "Missing item": "Order Support",
        "Refund request": "Refund Support",
    }).fillna("General Support")

    tickets["recommended_priority"] = tickets["predicted_ticket_type"].map({
        "Delayed order": "High",
        "Payment issue": "High",
        "Product quality": "High",
        "Missing item": "Medium",
        "Refund request": "Medium",
    }).fillna("Medium")

    tickets.to_csv(OUTPUT_DIR / "triaged_tickets.csv", index=False)

    results = {
        "test_accuracy": round(float(accuracy), 4),
        "test_ticket_count": int(len(y_test)),
        "classification_report": report,
        "note": (
            "Evaluation uses synthetic example tickets. "
            "Results do not establish real-world performance."
        ),
    }

    with open(
        OUTPUT_DIR / "triage_metrics.json", "w", encoding="utf-8"
    ) as file:
        json.dump(results, file, indent=2)

    print("Support ticket triage completed successfully!")
    print(f"Test accuracy: {accuracy:.3f}")
    print(f"Tickets processed: {len(tickets)}")
    print(f"Results saved to: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
