from pathlib import Path
import json
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

ROOT = Path(__file__).resolve().parents[1]
RAW_FILE = ROOT / "data" / "raw" / "Online Retail.xlsx"
PROCESSED = ROOT / "data" / "processed"
FIGURES = ROOT / "outputs" / "figures"
OUTPUTS = ROOT / "outputs"

def main():
    if not RAW_FILE.exists():
        raise FileNotFoundError(
            f"Dataset not found: {RAW_FILE}\nDownload Online Retail.xlsx from "
            "https://archive.ics.uci.edu/dataset/352/online+retail and place it in data/raw/."
        )

    PROCESSED.mkdir(parents=True, exist_ok=True)
    FIGURES.mkdir(parents=True, exist_ok=True)
    OUTPUTS.mkdir(parents=True, exist_ok=True)

    df = pd.read_excel(RAW_FILE)
    df.columns = [str(c).strip() for c in df.columns]
    required = {"InvoiceNo", "StockCode", "Description", "Quantity",
                "InvoiceDate", "UnitPrice", "CustomerID", "Country"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Unexpected dataset schema. Missing columns: {sorted(missing)}")

    initial_rows = len(df)
    missing_before = df.isna().sum().to_dict()
    duplicate_rows = int(df.duplicated().sum())

    df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"], errors="coerce")
    df["CustomerID"] = pd.to_numeric(df["CustomerID"], errors="coerce")
    df["Quantity"] = pd.to_numeric(df["Quantity"], errors="coerce")
    df["UnitPrice"] = pd.to_numeric(df["UnitPrice"], errors="coerce")

    # Keep a transparent sales-analysis table: require valid customer and transaction fields,
    # remove duplicate rows, cancellations, and non-positive quantity/price records.
    df = df.drop_duplicates()
    df = df.dropna(subset=["InvoiceNo", "InvoiceDate", "CustomerID", "Quantity", "UnitPrice"])
    df = df[~df["InvoiceNo"].astype(str).str.startswith("C", na=False)]
    df = df[(df["Quantity"] > 0) & (df["UnitPrice"] > 0)]
    df["CustomerID"] = df["CustomerID"].astype("int64")
    df["Sales"] = df["Quantity"] * df["UnitPrice"]
    df["InvoiceMonth"] = df["InvoiceDate"].dt.to_period("M").astype(str)

    clean_path = PROCESSED / "online_retail_clean.csv"
    df.to_csv(clean_path, index=False)

    db_path = PROCESSED / "retail.sqlite"
    with sqlite3.connect(db_path) as conn:
        df.to_sql("retail_transactions", conn, if_exists="replace", index=False, chunksize=100, method="multi")

    # Visualizations
    sns.set_theme()
    monthly = df.groupby("InvoiceMonth", as_index=False)["Sales"].sum()
    plt.figure(figsize=(12, 5))
    sns.lineplot(data=monthly, x="InvoiceMonth", y="Sales", marker="o")
    plt.title("Monthly Sales Revenue")
    plt.xlabel("Invoice month")
    plt.ylabel("Sales (dataset currency units)")
    plt.xticks(rotation=60, ha="right")
    plt.tight_layout()
    plt.savefig(FIGURES / "monthly_sales.png", dpi=160)
    plt.close()

    top_countries = (df.groupby("Country")["Sales"].sum()
                     .sort_values(ascending=False).head(10).sort_values())
    plt.figure(figsize=(10, 6))
    top_countries.plot(kind="barh")
    plt.title("Top 10 Countries by Sales")
    plt.xlabel("Sales (dataset currency units)")
    plt.ylabel("Country")
    plt.tight_layout()
    plt.savefig(FIGURES / "top_countries_sales.png", dpi=160)
    plt.close()

    customer_sales = df.groupby("CustomerID")["Sales"].sum()
    plt.figure(figsize=(10, 5))
    sns.histplot(customer_sales.clip(upper=customer_sales.quantile(0.99)), bins=40)
    plt.title("Customer Sales Distribution (clipped at 99th percentile for display)")
    plt.xlabel("Customer sales")
    plt.ylabel("Number of customers")
    plt.tight_layout()
    plt.savefig(FIGURES / "customer_sales_distribution.png", dpi=160)
    plt.close()

    summary = {
        "source": "UCI Online Retail dataset (downloaded by user)",
        "rows_before_cleaning": int(initial_rows),
        "rows_after_cleaning": int(len(df)),
        "duplicate_rows_before_cleaning": duplicate_rows,
        "missing_values_before_cleaning": {str(k): int(v) for k, v in missing_before.items()},
        "unique_customers": int(df["CustomerID"].nunique()),
        "unique_invoices": int(df["InvoiceNo"].nunique()),
        "unique_products": int(df["StockCode"].nunique()),
        "date_min": str(df["InvoiceDate"].min()),
        "date_max": str(df["InvoiceDate"].max()),
        "total_sales": round(float(df["Sales"].sum()), 2),
        "cleaning_notes": [
            "Removed exact duplicate rows.",
            "Removed rows missing invoice date, customer ID, invoice number, quantity, or unit price.",
            "Excluded invoice numbers beginning with C (cancellations/credit notes) from primary sales analysis.",
            "Excluded non-positive quantities and unit prices from primary sales analysis.",
            "Calculated Sales = Quantity * UnitPrice."
        ]
    }
    (OUTPUTS / "part1_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))
    print(f"\nSaved cleaned CSV: {clean_path}")
    print(f"Saved SQLite DB:   {db_path}")
    print(f"Saved charts in:   {FIGURES}")

if __name__ == "__main__":
    main()
