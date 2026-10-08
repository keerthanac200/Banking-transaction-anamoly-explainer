from fastapi import FastAPI
from pydantic import BaseModel
from app.anomaly_engine import analyze_transaction
from app.llm_explainer import generate_explanation

app = FastAPI(
    title="Banking Transaction Anomaly Explanation Generator",
    version="1.0"
)


class Transaction(BaseModel):
    transaction_id: str
    customer_id: str
    amount: float
    currency: str
    location: str
    transaction_time: str
    transaction_type: str
    merchant_category: str
    usual_transaction_amount: float
    usual_location: str
    anomaly: bool = False
    anomaly_codes: list[str] = []
    risk_score: float = 0.0
    rule_rationale: str = ""


def extract_ai_fields(ai_text):
    explanation = ai_text
    recommended_action = ""

    if "Suggested Action:" in ai_text:
        parts = ai_text.split("Suggested Action:", 1)
        explanation = parts[0].replace("Explanation:", "").strip()

        action_part = parts[1]

        if "Risk Level:" in action_part:
            recommended_action = action_part.split("Risk Level:", 1)[0].strip()
        else:
            recommended_action = action_part.strip()

    return explanation, recommended_action


@app.get("/")
def home():
    return {
        "status": "running",
        "service": "Banking Transaction Anomaly Explanation Generator"
    }


@app.post("/analyze")
def analyze(transaction: Transaction):
    transaction_data = transaction.model_dump()

    analysis = analyze_transaction(transaction_data)

    ai_text = generate_explanation(
        transaction_data,
        analysis
    )

    explanation, recommended_action = extract_ai_fields(ai_text)

    return {
        "transaction_id": transaction_data["transaction_id"],
        "customer_id": transaction_data["customer_id"],
        "amount": transaction_data["amount"],
        "location": transaction_data["location"],
        "usual_location": transaction_data["usual_location"],
        "transaction_time": transaction_data["transaction_time"],
        "transaction_type": transaction_data["transaction_type"],
        "merchant_category": transaction_data["merchant_category"],
        "risk_score": analysis["risk_score"],
        "anomaly_codes": analysis["anomaly_codes"],
        "explanation": explanation,
        "recommended_action": recommended_action
    }
