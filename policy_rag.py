
from pathlib import Path
import json

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


ROOT = Path(__file__).resolve().parent
POLICY_FILE = ROOT / "data" / "raw" / "policies.csv"
OUTPUT_DIR = ROOT / "outputs"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def retrieve_policy(question, policies, vectorizer, policy_vectors, top_k=2):
    """Retrieve the most relevant policy examples for a question."""
    question_vector = vectorizer.transform([question])
    scores = cosine_similarity(question_vector, policy_vectors).flatten()

    best_indices = scores.argsort()[::-1][:top_k]
    results = []

    for index in best_indices:
        results.append({
            "policy_id": str(policies.iloc[index]["policy_id"]),
            "topic": str(policies.iloc[index]["topic"]),
            "policy_text": str(policies.iloc[index]["policy_text"]),
            "similarity": round(float(scores[index]), 3),
        })

    return results


def answer_question(question, policies, vectorizer, policy_vectors):
    matches = retrieve_policy(
        question, policies, vectorizer, policy_vectors
    )

    # Avoid presenting weak matches as reliable policy guidance.
    if not matches or matches[0]["similarity"] < 0.05:
        return {
            "question": question,
            "answer": (
                "I could not find a sufficiently relevant policy. "
                "Please refer this case to a human support agent."
            ),
            "escalate_to_human": True,
            "retrieved_policies": matches,
        }

    best = matches[0]

    return {
        "question": question,
        "answer": (
            f"Relevant topic: {best['topic']}. "
            f"Reference guidance: {best['policy_text']} "
            "Check the actual order and payment records before "
            "making a decision. Escalate uncertain cases to a human."
        ),
        "escalate_to_human": True,
        "retrieved_policies": matches,
        "note": (
            "These are illustrative policies for a student project, "
            "not verified official Swiggy policies."
        ),
    }


def main():
    if not POLICY_FILE.exists():
        raise FileNotFoundError(
            f"Policy file not found: {POLICY_FILE}. "
            "Run python .\\generate_data.py first."
        )

    policies = pd.read_csv(POLICY_FILE).dropna(
        subset=["topic", "policy_text"]
    ).reset_index(drop=True)

    if policies.empty:
        raise ValueError("The policy file contains no usable policies.")

    documents = (
        policies["topic"].astype(str)
        + " "
        + policies["policy_text"].astype(str)
    )

    vectorizer = TfidfVectorizer(stop_words="english")
    policy_vectors = vectorizer.fit_transform(documents)

    questions = [
        "My delivery is late. Where is my order?",
        "Money was deducted but my order is missing.",
        "I received a damaged product.",
        "An item is missing from my delivery.",
        "How can I request a refund?",
        "I need help with an unrelated issue about my account.",
    ]

    results = [
        answer_question(q, policies, vectorizer, policy_vectors)
        for q in questions
    ]

    output_file = OUTPUT_DIR / "policy_rag_demo.json"
    with open(output_file, "w", encoding="utf-8") as file:
        json.dump(results, file, indent=2, ensure_ascii=False)

    print("Policy retrieval demo completed successfully!")
    print(f"Policies loaded: {len(policies)}")
    print(f"Questions tested: {len(questions)}")
    print(f"Results saved to: {output_file}")

    for result in results:
        topics = ", ".join(
            p["topic"] for p in result["retrieved_policies"]
        )
        print(f"\nQuestion: {result['question']}")
        print(f"Retrieved topics: {topics}")
        print(f"Human escalation: {result['escalate_to_human']}")


if __name__ == "__main__":
    main()
