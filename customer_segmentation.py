
from pathlib import Path
import json

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler

ROOT = Path(__file__).resolve().parent
DATA_DIR = ROOT / "data" / "raw"
OUTPUT_DIR = ROOT / "outputs"
FIGURE_DIR = OUTPUT_DIR / "figures"


def main():
    orders_file = DATA_DIR / "orders.csv"

    if not orders_file.exists():
        raise FileNotFoundError(
            "orders.csv not found. Run python .\\generate_data.py first."
        )

    orders = pd.read_csv(orders_file, parse_dates=["order_date"])

    required = {"customer_id", "order_date", "order_value", "order_id"}
    missing = required - set(orders.columns)
    if missing:
        raise ValueError(f"Missing columns: {sorted(missing)}")

    orders = orders.dropna(subset=list(required)).copy()
    orders["order_value"] = pd.to_numeric(
        orders["order_value"], errors="coerce"
    )
    orders = orders.dropna(subset=["order_value"])

    if orders.empty:
        raise ValueError("No usable orders found.")

    # RFM: Recency, Frequency, Monetary value
    reference_date = orders["order_date"].max().normalize() + pd.Timedelta(days=1)

    rfm = orders.groupby("customer_id").agg(
        recency_days=(
            "order_date",
            lambda dates: (reference_date - dates.max().normalize()).days,
        ),
        frequency=("order_id", "nunique"),
        monetary=("order_value", "sum"),
    ).reset_index()

    # Log transformation reduces the influence of very large values.
    features = rfm[["recency_days", "frequency", "monetary"]].copy()
    features = features.clip(lower=0) + 1
    features = features.apply(lambda column: __import__("numpy").log1p(column))

    scaler = StandardScaler()
    scaled_features = scaler.fit_transform(features)

    # Compare cluster counts using silhouette scores.
    scores = {}
    max_k = min(5, len(rfm) - 1)

    for k in range(2, max_k + 1):
        model = KMeans(n_clusters=k, random_state=42, n_init=10)
        labels = model.fit_predict(scaled_features)

        if len(set(labels)) > 1:
            scores[k] = silhouette_score(scaled_features, labels)

    if not scores:
        raise ValueError("Not enough customers to evaluate clusters.")

    best_k = max(scores, key=scores.get)

    final_model = KMeans(
        n_clusters=best_k, random_state=42, n_init=10
    )
    rfm["cluster"] = final_model.fit_predict(scaled_features)

    # Summarize each customer segment.
    summary = rfm.groupby("cluster").agg(
        customers=("customer_id", "nunique"),
        avg_recency_days=("recency_days", "mean"),
        avg_frequency=("frequency", "mean"),
        avg_monetary=("monetary", "mean"),
    ).reset_index()

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    FIGURE_DIR.mkdir(parents=True, exist_ok=True)

    rfm.to_csv(OUTPUT_DIR / "customer_rfm_segments.csv", index=False)
    summary.to_csv(OUTPUT_DIR / "customer_segment_summary.csv", index=False)

    # PCA: reduce the three RFM features to two dimensions for visualization.
    pca = PCA(n_components=2)
    coordinates = pca.fit_transform(scaled_features)

    plt.figure(figsize=(8, 5))
    points = plt.scatter(
        coordinates[:, 0],
        coordinates[:, 1],
        c=rfm["cluster"],
        alpha=0.75,
    )
    plt.xlabel("PCA component 1")
    plt.ylabel("PCA component 2")
    plt.title("Customer Segments — Synthetic Instamart-style Data")
    plt.colorbar(points, label="Cluster")
    plt.tight_layout()
    plt.savefig(FIGURE_DIR / "customer_segments_pca.png", dpi=150)
    plt.close()

    metrics = {
        "data_source": "Synthetic sample data; not actual Swiggy data",
        "customer_count": int(len(rfm)),
        "selected_k": int(best_k),
        "silhouette_scores": {
            str(k): round(float(score), 4)
            for k, score in scores.items()
        },
        "pca_explained_variance_ratio": [
            round(float(value), 4)
            for value in pca.explained_variance_ratio_
        ],
        "pca_total_explained_variance": round(
            float(pca.explained_variance_ratio_.sum()), 4
        ),
    }

    (OUTPUT_DIR / "customer_segmentation_metrics.json").write_text(
        json.dumps(metrics, indent=2),
        encoding="utf-8",
    )

    print("Customer segmentation completed successfully!")
    print(f"Customers analyzed: {len(rfm)}")
    print(f"Selected clusters: {best_k}")
    print("Silhouette scores:")
    for k, score in scores.items():
        print(f"  k={k}: {score:.3f}")
    print(
        "PCA variance explained: "
        f"{metrics['pca_total_explained_variance']:.1%}"
    )
    print("Results saved in the outputs folder.")


if __name__ == "__main__":
    main()
