import streamlit as st

st.set_page_config(
    page_title="Banking Anomaly Explainer",
    page_icon="🏦",
    layout="wide"
)

# ---------- HEADER ----------
st.title("🏦 Banking Transaction Anomaly Explainer")
st.caption("AI-powered detection and explanation of suspicious transactions")

st.divider()

# ---------- TRANSACTION SELECTOR ----------
st.subheader("🔎 Transaction Analysis")

transaction_id = st.selectbox(
    "Select Transaction",
    ["TXN1001", "TXN1002", "TXN1003"]
)

# ---------- TRANSACTION DATA ----------
transactions = {
    "TXN1001": {
        "customer": "CUST501",
        "amount": 85000,
        "location": "Bengaluru",
        "usual_location": "Mysuru",
        "time": "02:13 AM",
        "type": "CARD_PAYMENT",
        "merchant": "Electronics",
        "risk": 91,
        "anomalies": [
            "HIGH AMOUNT",
            "UNUSUAL LOCATION",
            "UNUSUAL TIME"
        ],
        "explanation": (
            "The transaction amount of ₹85,000 is substantially higher "
            "than the customer's usual transaction amount of ₹4,500. "
            "The transaction also occurred in Bengaluru, while the "
            "customer's usual location is Mysuru, at an unusual time "
            "of 2:13 AM."
        ),
        "action": (
            "Verify the transaction with the customer. If it is not "
            "recognized, temporarily block the card/account and "
            "initiate a fraud investigation."
        )
    },

    "TXN1002": {
        "customer": "CUST502",
        "amount": 2400,
        "location": "Mysuru",
        "usual_location": "Mysuru",
        "time": "07:30 PM",
        "type": "CARD_PAYMENT",
        "merchant": "Grocery",
        "risk": 18,
        "anomalies": [],
        "explanation": (
            "The transaction is consistent with the customer's "
            "normal spending amount, location and transaction time."
        ),
        "action": "No immediate action required."
    },

    "TXN1003": {
        "customer": "CUST503",
        "amount": 45000,
        "location": "Chennai",
        "usual_location": "Bengaluru",
        "time": "01:42 AM",
        "type": "ONLINE_PAYMENT",
        "merchant": "Luxury Goods",
        "risk": 84,
        "anomalies": [
            "HIGH AMOUNT",
            "UNUSUAL LOCATION",
            "UNUSUAL TIME"
        ],
        "explanation": (
            "The transaction amount is significantly higher than "
            "the customer's typical spending pattern. The location "
            "and transaction time also differ from the customer's "
            "usual behavior."
        ),
        "action": (
            "Contact the customer to verify the transaction. "
            "Consider temporarily restricting the account if "
            "the customer does not recognize it."
        )
    }
}

data = transactions[transaction_id]

# ---------- TRANSACTION DETAILS ----------
st.subheader("💳 Transaction Details")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Customer", data["customer"])

with col2:
    st.metric("Amount", f"₹{data['amount']:,}")

with col3:
    st.metric("Location", data["location"])

with col4:
    st.metric("Transaction Type", data["type"])

# Extra information
col1, col2, col3 = st.columns(3)

with col1:
    st.write("**Merchant Category**")
    st.write(data["merchant"])

with col2:
    st.write("**Transaction Time**")
    st.write(data["time"])

with col3:
    st.write("**Usual Location**")
    st.write(data["usual_location"])

st.divider()

# ---------- RISK ASSESSMENT ----------
st.subheader("🚨 Risk Assessment")

risk = data["risk"]

col1, col2 = st.columns([1, 2])

with col1:
    st.metric("Risk Score", f"{risk}%")

    if risk >= 70:
        st.error("🔴 HIGH RISK")
    elif risk >= 40:
        st.warning("🟠 MEDIUM RISK")
    else:
        st.success("🟢 LOW RISK")

with col2:
    st.write("**Detected Anomalies**")

    if data["anomalies"]:
        for anomaly in data["anomalies"]:
            st.error(f"⚠️ {anomaly}")
    else:
        st.success("✓ No significant anomalies detected")

st.divider()

# ---------- AI EXPLANATION ----------
st.subheader("🤖 AI-Generated Explanation")

st.info(data["explanation"])

st.divider()

# ---------- RECOMMENDATION ----------
st.subheader("💡 Recommended Action")

if risk >= 70:
    st.warning(data["action"])
elif risk >= 40:
    st.info(data["action"])
else:
    st.success(data["action"])

st.divider()

# ---------- FOOTER ----------
st.caption(
    "Prototype • Banking Transaction Anomaly Explanation Generator"
)