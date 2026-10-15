import json
import subprocess


def generate_explanation(transaction, analysis):
    prompt = f"""
You are a banking transaction anomaly explanation assistant.

Explain the transaction ONLY using the information provided below.
Do not invent facts.

Transaction:
{json.dumps(transaction, indent=2)}

Detected anomaly:
{json.dumps(analysis, indent=2)}

Return exactly this format:

Explanation:
<2-3 sentence explanation of why the transaction was flagged>

Suggested Action:
<one practical action for a bank analyst>

Risk Level:
<LOW, MEDIUM, or HIGH>
"""

    result = subprocess.run(
        ["ollama", "run", "gemma3:4b", prompt],
        capture_output=True,
        text=True,
        encoding="utf-8"
    )

    if result.returncode != 0:
        return f"Ollama error: {result.stderr}"

    return result.stdout.strip()


if __name__ == "__main__":
    with open("data/transactions.json", "r", encoding="utf-8-sig") as f:
        transactions = json.load(f)

    from anomaly_engine import analyze_transaction

    transaction = transactions[0]
    analysis = analyze_transaction(transaction)

    print("\n===== AI EXPLANATION =====\n")
    print(generate_explanation(transaction, analysis))
