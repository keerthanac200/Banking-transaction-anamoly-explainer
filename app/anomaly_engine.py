import json

def analyze_transaction(tx):
    reasons = []
    score = 0.0

    if tx["amount"] > tx["usual_transaction_amount"] * 5:
        reasons.append("HIGH_AMOUNT")
        score += 0.35

    if tx["location"] != tx["usual_location"]:
        reasons.append("UNUSUAL_LOCATION")
        score += 0.25

    hour = int(tx["transaction_time"][11:13])
    if hour < 6 or hour >= 23:
        reasons.append("UNUSUAL_TIME")
        score += 0.20

    unusual_categories = ["Jewellery", "Gambling", "Cryptocurrency"]
    if tx["merchant_category"] in unusual_categories:
        reasons.append("UNUSUAL_MERCHANT_CATEGORY")
        score += 0.15

    score = min(score, 0.99)

    return {
        "transaction_id": tx["transaction_id"],
        "is_anomaly": len(reasons) > 0,
        "anomaly_codes": reasons,
        "risk_score": round(score, 2),
        "rule_rationale": tx.get("rule_rationale", "")
    }


def analyze_all():
    with open("data/transactions.json", "r", encoding="utf-8-sig") as f:
        transactions = json.load(f)

    results = [analyze_transaction(tx) for tx in transactions]

    return results


if __name__ == "__main__":
    results = analyze_all()

    print("\n===== ANOMALY DETECTION RESULTS =====\n")

    for result in results:
        print(f"Transaction: {result['transaction_id']}")
        print(f"Anomaly: {result['is_anomaly']}")
        print(f"Reasons: {', '.join(result['anomaly_codes']) or 'None'}")
        print(f"Risk Score: {result['risk_score']}")
        print("-" * 50)
