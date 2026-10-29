
from pathlib import Path
import random
import pandas as pd

# Reproducible synthetic data — not actual Swiggy customer data.
random.seed(42)

ROOT = Path(__file__).resolve().parent
DATA_DIR = ROOT / "data" / "raw"
DATA_DIR.mkdir(parents=True, exist_ok=True)

cities = ["Bengaluru", "Chennai", "Hyderabad", "Mumbai", "Pune", "Delhi"]
products = [
    ("Milk", 32), ("Bread", 40), ("Eggs", 75), ("Rice", 90),
    ("Bananas", 50), ("Apples", 120), ("Curd", 35),
    ("Cooking Oil", 150), ("Biscuits", 25), ("Detergent", 110)
]
categories = {
    "Milk": "Dairy", "Bread": "Bakery", "Eggs": "Dairy",
    "Rice": "Staples", "Bananas": "Fruits", "Apples": "Fruits",
    "Curd": "Dairy", "Cooking Oil": "Staples",
    "Biscuits": "Snacks", "Detergent": "Household"
}
statuses = ["Delivered", "Delayed", "Cancelled"]
ticket_types = [
    "Delayed order", "Payment issue", "Product quality",
    "Missing item", "Refund request"
]

# 1. Customers
customers = []
for i in range(1, 501):
    customers.append({
        "customer_id": f"C{i:04d}",
        "city": random.choice(cities),
        "signup_date": (
            pd.Timestamp("2025-01-01")
            + pd.Timedelta(days=random.randint(0, 600))
        ).date().isoformat(),
        "age": random.randint(18, 70),
        "loyalty_tier": random.choice(["Regular", "Silver", "Gold"]),
    })

customers_df = pd.DataFrame(customers)

# 2. Orders and order items
orders = []
for i in range(1, 2001):
    customer = random.choice(customers)
    product, price = random.choice(products)
    quantity = random.randint(1, 5)
    status = random.choices(
        statuses, weights=[0.86, 0.10, 0.04], k=1
    )[0]
    order_date = (
        pd.Timestamp("2026-01-01")
        + pd.Timedelta(days=random.randint(0, 300))
    )
    orders.append({
        "order_id": f"O{i:05d}",
        "customer_id": customer["customer_id"],
        "order_date": order_date.date().isoformat(),
        "product": product,
        "category": categories[product],
        "quantity": quantity,
        "unit_price": price,
        "order_value": quantity * price,
        "status": status,
        "delivery_minutes": (
            random.randint(10, 25) if status == "Delivered"
            else random.randint(26, 90)
        ),
    })

orders_df = pd.DataFrame(orders)

# 3. Support tickets
tickets = []
for i in range(1, 401):
    ticket_type = random.choice(ticket_types)
    tickets.append({
        "ticket_id": f"T{i:04d}",
        "customer_id": random.choice(customers)["customer_id"],
        "ticket_type": ticket_type,
        "description": {
            "Delayed order": "My order has not arrived on time.",
            "Payment issue": "My payment was deducted but the order is missing.",
            "Product quality": "The product arrived damaged or poor quality.",
            "Missing item": "One item is missing from my order.",
            "Refund request": "Please help me with a refund for my order.",
        }[ticket_type],
        "priority": random.choice(["Low", "Medium", "High"]),
        "status": random.choice(["Open", "In Progress", "Resolved"]),
    })

tickets_df = pd.DataFrame(tickets)

# 4. Clearly labelled illustrative policies, not official Swiggy policies.
policies = pd.DataFrame([
    {
        "policy_id": "P001",
        "topic": "Delayed orders",
        "policy_text": (
            "Illustrative rule: verify the order status and estimated "
            "arrival time. Escalate repeated or severe delays to support."
        ),
    },
    {
        "policy_id": "P002",
        "topic": "Refund requests",
        "policy_text": (
            "Illustrative rule: verify the order, payment, and issue "
            "before deciding eligibility. Refer uncertain cases to a human."
        ),
    },
    {
        "policy_id": "P003",
        "topic": "Damaged products",
        "policy_text": (
            "Illustrative rule: record the affected item and issue details. "
            "Escalate disputed or unclear cases to a human agent."
        ),
    },
    {
        "policy_id": "P004",
        "topic": "Missing items",
        "policy_text": (
            "Illustrative rule: compare the order items with the reported "
            "missing item and refer unresolved cases to support."
        ),
    },
    {
        "policy_id": "P005",
        "topic": "Payment issues",
        "policy_text": (
            "Illustrative rule: verify payment and order records before "
            "giving guidance. Never claim a refund was issued without proof."
        ),
    },
])

# Save all datasets as CSV files.
customers_df.to_csv(DATA_DIR / "customers.csv", index=False)
orders_df.to_csv(DATA_DIR / "orders.csv", index=False)
tickets_df.to_csv(DATA_DIR / "tickets.csv", index=False)
policies.to_csv(DATA_DIR / "policies.csv", index=False)

print("Synthetic Instamart-style data created successfully.")
print(f"Customers: {len(customers_df)}")
print(f"Orders: {len(orders_df)}")
print(f"Tickets: {len(tickets_df)}")
print(f"Policies: {len(policies)}")
print(f"Saved in: {DATA_DIR}")
print("Note: These are synthetic examples, not real Swiggy data.")
