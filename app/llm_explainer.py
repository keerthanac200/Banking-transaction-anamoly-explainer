import requests
import re

OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "gemma3:4b"
OLLAMA_TIMEOUT = 180


def generate_explanation(transaction, analysis):
    """Generate a complete, concise explanation with a reliable fallback."""

    anomaly_codes = analysis.get("anomaly_codes", [])
    risk_score = analysis.get("risk_score", 0)

    try:
        risk_score = float(risk_score)
    except (TypeError, ValueError):
        risk_score = 0.0

    if risk_score >= 0.70:
        risk_level = "HIGH"
    elif risk_score >= 0.40:
        risk_level = "MEDIUM"
    else:
        risk_level = "LOW"

    amount = transaction.get("amount", "unknown")
    usual_amount = transaction.get("usual_transaction_amount", "unknown")
    location = transaction.get("location", "unknown")
    usual_location = transaction.get("usual_location", "unknown")

    # Build an evidence-based explanation without relying on the LLM.
    reasons = []

    if "HIGH_AMOUNT" in anomaly_codes:
        reasons.append(
            f"The transaction amount ({amount}) is higher than "
            f"the customer's usual transaction amount ({usual_amount})."
        )

    if "UNUSUAL_LOCATION" in anomaly_codes:
        reasons.append(
            f"The transaction location ({location}) differs from "
            f"the customer's usual location ({usual_location})."
        )

    if "UNUSUAL_TIME" in anomaly_codes:
        reasons.append(
            "The transaction occurred at an unusual time."
        )

    if "UNUSUAL_MERCHANT_CATEGORY" in anomaly_codes:
        reasons.append(
            "The merchant category triggered an anomaly indicator."
        )

    if not reasons:
        reasons.append(
            "The transaction was flagged by the anomaly detection system."
        )

    fallback_explanation = " ".join(reasons)

    if risk_level in ("HIGH", "MEDIUM"):
        fallback_action = (
            "Review the transaction details and verify the activity "
            "with the customer before taking further action."
        )
    else:
        fallback_action = (
            "Continue routine monitoring and follow standard "
            "banking review procedures."
        )

    fallback = (
        f"Explanation: {fallback_explanation}\n\n"
        f"Suggested Action: {fallback_action}\n\n"
        f"Risk Level: {risk_level}"
    )

    prompt = f"""
You are BankGuard AI, a banking transaction explanation assistant.

Use ONLY the facts supplied below. Never invent information.
An anomaly is a reason to review a transaction, not proof of fraud.

Transaction amount: {amount}
Customer's usual transaction amount: {usual_amount}
Transaction location: {location}
Customer's usual location: {usual_location}
Anomaly indicators: {", ".join(anomaly_codes) if anomaly_codes else "None"}
Calculated risk score: {risk_score}
Calculated risk level: {risk_level}

Write a complete response using EXACTLY these three headings:

Explanation:
Write 2 or 3 complete sentences explaining the supplied indicators.

Suggested Action:
Write 1 or 2 complete sentences describing a sensible review action.

Risk Level:
Write exactly {risk_level}.

Requirements:
- Use clear, professional banking language.
- Complete every sentence.
- Do not repeat the same point.
- Do not claim fraud is confirmed.
- Do not change the calculated risk level.
- Keep the complete response under 120 words.
- Do not end in the middle of a sentence.
"""

    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": OLLAMA_MODEL,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "num_predict": 180,
                    "temperature": 0.1,
                },
            },
            timeout=OLLAMA_TIMEOUT,
        )

        response.raise_for_status()

        explanation = response.json().get("response", "").strip()

        # Remove any accidental surrounding Markdown fences.
        explanation = re.sub(
            r"^\s*```(?:text|markdown)?\s*|\s*```\s*$",
            "",
            explanation,
            flags=re.IGNORECASE,
        ).strip()

        # Validate that all required sections are present.
        has_explanation = re.search(
            r"(?im)^\s*Explanation\s*:",
            explanation,
        )
        has_action = re.search(
            r"(?im)^\s*Suggested Action\s*:",
            explanation,
        )
        has_risk = re.search(
            r"(?im)^\s*Risk Level\s*:",
            explanation,
        )

        # Reject incomplete responses rather than showing broken output.
        if has_explanation and has_action and has_risk:
            risk_match = re.search(
                r"(?im)^\s*Risk Level\s*:\s*(HIGH|MEDIUM|LOW)\b",
                explanation,
            )

            if risk_match:
                # Keep the risk level consistent with the rule engine.
                explanation = re.sub(
                    r"(?im)^(\s*Risk Level\s*:\s*)(HIGH|MEDIUM|LOW)\b.*$",
                    lambda match: match.group(1) + risk_level,
                    explanation,
                )

                print("[LLM] Complete explanation generated.")
                return explanation

        print("[LLM] Response incomplete. Using rule-based fallback.")

    except requests.Timeout:
        print(
            f"[LLM] Ollama exceeded {OLLAMA_TIMEOUT} seconds. "
            "Using rule-based fallback."
        )

    except requests.RequestException as error:
        print(f"[LLM] Ollama request failed: {error}. Using fallback.")

    except (ValueError, KeyError) as error:
        print(f"[LLM] Invalid Ollama response: {error}. Using fallback.")

    return fallback


if __name__ == "__main__":
    print("BankGuard AI LLM explainer loaded.")
    print(f"Model: {OLLAMA_MODEL}")
    print(f"Ollama URL: {OLLAMA_URL}")
    print(f"Timeout: {OLLAMA_TIMEOUT} seconds")