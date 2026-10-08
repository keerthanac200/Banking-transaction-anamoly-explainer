import streamlit as st

st.set_page_config(
    page_title="Banking Transaction Anomaly Explainer",
    page_icon="🏦",
    layout="wide"
)

# Header
st.title("🏦 Banking Transaction Anomaly Explainer")
st.caption("AI-powered explanation of suspicious banking transactions")

st.divider()

# Transaction Details
st.subheader("💳 Transaction Details")

col1, col2 = st.columns(2)

with col1:
    st.text_input("Transaction ID", "TXN1001")
    st.number_input("Transaction Amount (₹)", value=85000)
    st.text_input("Location", "Bengaluru")

with col2:
    st.text_input("Customer ID", "CUST501")
    st.text_input("Transaction Type", "CARD_PAYMENT")
    st.text_input("Merchant Category", "Electronics")

st.divider()

# Anomaly Detection
st.subheader("🚨 Anomaly Detection")

st.error("⚠️ Anomaly Detected")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Risk Score", "91%")

with col2:
    st.metric("Amount Anomaly", "YES")

with col3:
    st.metric("Location Anomaly", "YES")

st.divider()

# AI Explanation
st.subheader("🤖 AI Explanation")

st.info(
    "This transaction was flagged because the amount of ₹85,000 "
    "is substantially higher than the customer's usual transaction "
    "amount of ₹4,500. The transaction also occurred in Bengaluru, "
    "while the customer's usual location is Mysuru."
)

# Recommended Action
st.subheader("💡 Recommended Action")

st.warning(
    "Verify the transaction with the customer. If the transaction "
    "is not recognized, temporarily block the card/account and "
    "initiate a fraud investigation."
)