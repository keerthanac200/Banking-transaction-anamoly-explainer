import json
import os
from datetime import datetime

import requests
import streamlit as st


# ============================================================
# CONFIGURATION
# ============================================================

API_URL = os.getenv("BANKGUARD_API_URL", "http://127.0.0.1:8000")
ANALYZE_URL = f"{API_URL.rstrip('/')}/analyze"

st.set_page_config(
    page_title="BankGuard AI",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>
    @import url(
        'https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap'
    );

    :root {
        --bg: #0b1020;
        --panel: #121a2b;
        --panel-light: #182338;
        --border: #27344b;
        --text: #edf2ff;
        --muted: #9aa9c2;
        --accent: #7c8cff;
        --green: #36d399;
        --red: #fb7185;
        --orange: #fbbf24;
    }

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    .stApp {
        background:
            radial-gradient(
                ellipse at 10% 0%,
                rgba(72, 94, 180, 0.15),
                transparent 35%
            ),
            var(--bg);
        color: var(--text);
    }

    [data-testid="stHeader"] {
        background: rgba(11, 16, 32, 0.9);
    }

    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #111a2c 0%, #0c1322 100%);
        border-right: 1px solid var(--border);
    }

    [data-testid="stSidebar"] > div:first-child {
        padding-top: 1.4rem;
    }

    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {
        color: var(--muted);
    }

    [data-testid="stSidebar"] .stRadio > div {
        gap: 8px;
    }

    [data-testid="stSidebar"] .stRadio label {
        background: rgba(255, 255, 255, 0.025);
        border: 1px solid transparent;
        border-radius: 10px;
        padding: 10px 12px;
        transition: all 0.2s ease;
    }

    [data-testid="stSidebar"] .stRadio label:hover {
        background: rgba(124, 140, 255, 0.10);
        border-color: var(--border);
    }

    [data-testid="stSidebar"] .stRadio label p {
        color: var(--text) !important;
        font-weight: 500;
    }

    h1, h2, h3 {
        color: var(--text) !important;
        letter-spacing: -0.5px;
    }

    p, label, span {
        color: var(--text);
    }

    .brand {
        font-size: 1.75rem;
        font-weight: 800;
        letter-spacing: -1px;
        margin-bottom: 0;
        color: #ffffff;
    }

    .brand-accent {
        color: var(--accent);
    }

    .subtitle {
        color: var(--muted);
        font-size: 0.95rem;
        line-height: 1.65;
    }

    .hero {
        background:
            linear-gradient(
                120deg,
                rgba(124, 140, 255, 0.15),
                rgba(54, 211, 153, 0.045)
            );
        border: 1px solid var(--border);
        border-radius: 20px;
        padding: 30px;
        margin: 10px 0 24px 0;
    }

    .hero h1 {
        font-size: clamp(2rem, 4vw, 3.2rem);
        font-weight: 800;
        margin-bottom: 10px;
    }

    .hero p {
        color: var(--muted);
        font-size: 1.03rem;
        line-height: 1.7;
        max-width: 800px;
    }

    .eyebrow {
        display: inline-block;
        padding: 6px 10px;
        border: 1px solid rgba(124, 140, 255, 0.4);
        border-radius: 30px;
        color: #b9c2ff;
        background: rgba(124, 140, 255, 0.09);
        font-size: 0.78rem;
        font-weight: 700;
        letter-spacing: 1px;
        margin-bottom: 14px;
    }

    .metric-card {
        background: linear-gradient(145deg, #172238, #111a2b);
        border: 1px solid var(--border);
        border-radius: 15px;
        padding: 20px;
        min-height: 125px;
    }

    .metric-label {
        color: var(--muted);
        font-size: 0.85rem;
        margin-bottom: 10px;
    }

    .metric-value {
        color: #ffffff;
        font-size: 1.8rem;
        font-weight: 800;
    }

    .panel {
        background: var(--panel);
        border: 1px solid var(--border);
        border-radius: 16px;
        padding: 22px;
        margin: 12px 0;
    }

    .panel-title {
        font-size: 1.1rem;
        font-weight: 700;
        margin-bottom: 8px;
    }

    .muted {
        color: var(--muted);
    }

    .status {
        display: inline-block;
        padding: 8px 13px;
        border-radius: 30px;
        font-size: 0.84rem;
        font-weight: 700;
    }

    .status-danger {
        color: #fecdd3;
        background: rgba(251, 113, 133, 0.13);
        border: 1px solid rgba(251, 113, 133, 0.35);
    }

    .status-safe {
        color: #a7f3d0;
        background: rgba(54, 211, 153, 0.12);
        border: 1px solid rgba(54, 211, 153, 0.3);
    }

    .status-warning {
        color: #fde68a;
        background: rgba(251, 191, 36, 0.12);
        border: 1px solid rgba(251, 191, 36, 0.3);
    }

    .step-card {
        background: var(--panel);
        border: 1px solid var(--border);
        border-radius: 14px;
        padding: 20px;
        height: 100%;
    }

    .step-number {
        display: inline-flex;
        width: 38px;
        height: 38px;
        align-items: center;
        justify-content: center;
        background: rgba(124, 140, 255, 0.15);
        color: #b9c2ff;
        border-radius: 11px;
        font-weight: 800;
        margin-bottom: 12px;
    }

    .step-title {
        font-weight: 700;
        margin-bottom: 8px;
    }

    div.stButton > button,
    div.stFormSubmitButton > button {
        background: linear-gradient(100deg, #6878f5, #8b76f8);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.65rem 1.2rem;
        font-weight: 700;
        transition: all 0.2s ease;
    }

    div.stButton > button:hover,
    div.stFormSubmitButton > button:hover {
        color: white;
        border: none;
        filter: brightness(1.12);
        transform: translateY(-1px);
    }

    div[data-testid="stTextInput"] input,
    div[data-testid="stNumberInput"] input,
    div[data-testid="stDateInput"] input,
    div[data-testid="stTimeInput"] input,
    div[data-testid="stSelectbox"] > div,
    div[data-testid="stTextArea"] textarea {
        background-color: #101a2c;
        border-color: var(--border);
        border-radius: 9px;
        color: var(--text);
    }

    div[data-testid="stMetric"] {
        background: var(--panel);
        border: 1px solid var(--border);
        padding: 15px;
        border-radius: 12px;
    }

    div[data-testid="stMetricLabel"] {
        color: var(--muted);
    }

    hr {
        border-color: var(--border);
    }

    .footer {
        text-align: center;
        color: var(--muted);
        font-size: 0.8rem;
        padding: 25px 0 10px 0;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# SESSION STATE
# ============================================================

if "history" not in st.session_state:
    st.session_state.history = []

if "last_result" not in st.session_state:
    st.session_state.last_result = None

if "page" not in st.session_state:
    st.session_state.page = "Home"


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def mask_id(value):
    """Mask an ID for display while preserving its prefix and last two characters."""
    if value is None:
        return "N/A"

    value = str(value).strip()

    if not value:
        return "N/A"

    if len(value) <= 4:
        return "*" * len(value)

    visible_start = min(5, len(value) - 2)
    visible_end = 2
    hidden_length = len(value) - visible_start - visible_end

    return (
        value[:visible_start]
        + "*" * hidden_length
        + value[-visible_end:]
    )

def money(value, currency="INR"):
    """Format a transaction amount."""
    try:
        return f"{currency} {float(value):,.2f}"
    except (TypeError, ValueError):
        return f"{currency} {value}"


def normalize_risk_score(value):
    """
    Accept risk scores represented as either 0-1 or 0-100.
    Return a percentage between 0 and 100.
    """
    try:
        score = float(value)
    except (TypeError, ValueError):
        return 0.0

    if score <= 1:
        score *= 100

    return max(0.0, min(score, 100.0))


def get_risk_label(score):
    if score >= 70:
        return "HIGH"
    if score >= 35:
        return "MEDIUM"
    return "LOW"


def get_anomaly_status(result):
    """Read common anomaly response key names."""
    for key in ("is_anomaly", "anomaly", "flagged"):
        if key in result:
            value = result[key]

            if isinstance(value, str):
                return value.strip().lower() in (
                    "true", "yes", "1", "anomaly", "flagged"
                )

            return bool(value)

    return False


def get_explanation(result):
    """Extract the explanation from common backend response formats."""
    for key in (
        "explanation",
        "ai_explanation",
        "llm_explanation",
        "generated_explanation",
        "rule_rationale",
        "reason",
    ):
        value = result.get(key)

        if value:
            if isinstance(value, dict):
                return json.dumps(value, indent=2, ensure_ascii=False)
            return str(value)

    return "No explanation was returned by the backend."


def get_anomaly_codes(result):
    codes = result.get(
        "anomaly_codes",
        result.get("anomaly_reasons", result.get("reasons", [])),
    )

    if isinstance(codes, str):
        return [codes] if codes.strip() else []

    if isinstance(codes, list):
        return codes

    return []


def analyze_transaction(payload):
    """Send a transaction to the FastAPI backend."""
    try:
        response = requests.post(
            ANALYZE_URL,
            json=payload,
            timeout=150,
        )

        if not response.ok:
            message = response.text[:1500]
            st.error(
                f"Backend returned HTTP {response.status_code}."
            )
            with st.expander("Technical details"):
                st.code(message)
            return None

        result = response.json()

        if not isinstance(result, dict):
            st.error("The backend returned an unexpected response format.")
            return None

        result.setdefault("transaction_id", payload["transaction_id"])
        result.setdefault("customer_id", payload["customer_id"])
        result.setdefault("amount", payload["amount"])
        result.setdefault("currency", payload["currency"])
        result.setdefault("location", payload["location"])
        result.setdefault("transaction_time", payload["transaction_time"])
        result.setdefault("transaction_type", payload["transaction_type"])
        result.setdefault("merchant_category", payload["merchant_category"])

        result["_submitted_payload"] = payload
        result["_analyzed_at"] = datetime.now().strftime(
            "%d %b %Y, %I:%M:%S %p"
        )

        st.session_state.last_result = result
        st.session_state.history.insert(0, result)

        return result

    except requests.exceptions.ConnectionError:
        st.error(
            "Could not connect to the backend. Make sure your FastAPI "
            "server is running at http://127.0.0.1:8000."
        )
        st.info(
            "Start the backend in a separate terminal before analyzing "
            "a transaction."
        )
        return None

    except requests.exceptions.Timeout:
        st.error(
            "The request timed out. The AI explanation model may still "
            "be processing. Please check the backend terminal."
        )
        return None

    except ValueError:
        st.error("The backend response was not valid JSON.")
        return None

    except requests.exceptions.RequestException as exc:
        st.error(f"Request failed: {exc}")
        return None


def render_result(result):
    """Display the analysis returned by the backend."""
    anomaly = get_anomaly_status(result)

    score_raw = result.get(
        "risk_score",
        result.get("risk", 0),
    )
    score = normalize_risk_score(score_raw)
    risk_label = get_risk_label(score)

    st.markdown("---")
    st.subheader("Analysis Results")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(
            '<div class="metric-card">'
            '<div class="metric-label">Transaction Status</div>'
            f'<div style="margin-top:12px">'
            f'<span class="status {"status-danger" if anomaly else "status-safe"}">'
            f'{"⚠️ Anomaly Detected" if anomaly else "✓ No Anomaly Detected"}'
            '</span></div></div>',
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            '<div class="metric-card">'
            '<div class="metric-label">Risk Score</div>'
            f'<div class="metric-value">{score:.1f}%</div>'
            '</div>',
            unsafe_allow_html=True,
        )

    with col3:
        risk_class = (
            "status-danger" if risk_label == "HIGH"
            else "status-warning" if risk_label == "MEDIUM"
            else "status-safe"
        )

        st.markdown(
            '<div class="metric-card">'
            '<div class="metric-label">Risk Level</div>'
            f'<div style="margin-top:12px">'
            f'<span class="status {risk_class}">{risk_label}</span>'
            '</div></div>',
            unsafe_allow_html=True,
        )

    st.write("")
    st.progress(int(score), text=f"Risk score: {score:.1f}%")

    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown("### 🧠 Transaction Explanation")

    explanation = get_explanation(result)
    st.write(explanation)

    st.markdown("</div>", unsafe_allow_html=True)

    codes = get_anomaly_codes(result)

    st.markdown("### 🔎 Detected Indicators")

    if codes:
        indicator_columns = st.columns(min(len(codes), 3))

        for index, code in enumerate(codes):
            with indicator_columns[index % len(indicator_columns)]:
                st.warning(str(code))
    elif anomaly:
        st.info(
            "The backend flagged this transaction but did not provide "
            "specific anomaly codes."
        )
    else:
        st.success("No anomaly indicators were returned.")

    rationale = result.get("rule_rationale")

    if rationale and rationale != explanation:
        with st.expander("View rule-engine rationale"):
            st.write(rationale)

    suggested_action = (
        result.get("suggested_action")
        or result.get("recommended_action")
    )

    if suggested_action:
        st.markdown("### 💡 Suggested Action")
        st.info(str(suggested_action))

    st.caption(
        "This result is a decision-support signal, not proof of fraud. "
        "Review flagged transactions before taking action."
    )

    with st.expander("View raw backend response"):
        display_result = {
            key: value
            for key, value in result.items()
            if not key.startswith("_")
        }

        if "transaction_id" in display_result:
            display_result["transaction_id"] = mask_id(
                display_result["transaction_id"]
            )

        if "customer_id" in display_result:
            display_result["customer_id"] = mask_id(
                display_result["customer_id"]
            )

        st.json(display_result)


def render_metric_card(label, value):
    st.markdown(
        '<div class="metric-card">'
        f'<div class="metric-label">{label}</div>'
        f'<div class="metric-value">{value}</div>'
        '</div>',
        unsafe_allow_html=True,
    )


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:
    st.markdown(
        """
        <div style="padding: 5px 5px 18px 5px;">
            <div style="font-size:2.2rem;">🛡️</div>
            <div class="brand">BankGuard<span class="brand-accent"> AI</span></div>
            <div class="subtitle">Intelligent Transaction Security</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("---")
    st.markdown("##### NAVIGATION")

    page = st.radio(
        "Navigate",
        [
            "Home",
            "Analyze Transaction",
            "Transaction History",
            "About Project",
        ],
        label_visibility="collapsed",
        key="page",
    )

    st.markdown("---")

    st.markdown("##### SYSTEM STATUS")

    try:
        health_response = requests.get(
            f"{API_URL.rstrip('/')}/",
            timeout=2,
        )

        if health_response.ok:
            st.success("Backend reachable")
        else:
            st.warning(f"Backend responded: {health_response.status_code}")

    except requests.exceptions.RequestException:
        st.error("Backend unavailable")

    st.caption(f"API endpoint: {API_URL}")

    st.markdown("---")

    st.markdown(
        """
        <div style="font-size:0.78rem; line-height:1.7;">
            <span style="color:#9aa9c2;">POWERED BY</span><br>
            <b>FastAPI</b> · <b>Streamlit</b> · <b>AI / Ollama</b>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# HOME PAGE
# ============================================================

if page == "Home":

    st.markdown(
        """
        <div class="hero">
            <div class="eyebrow">AI-POWERED FINANCIAL SECURITY</div>
            <h1>Welcome to BankGuard AI 🛡️</h1>
            <p>
                Detect suspicious banking transactions, understand potential
                risks, and generate AI-assisted explanations using a
                rule-based anomaly engine and a language model.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    total = len(st.session_state.history)
    anomalies = sum(
        get_anomaly_status(item)
        for item in st.session_state.history
    )
    normal = total - anomalies

    c1, c2, c3 = st.columns(3)

    with c1:
        render_metric_card("Transactions Analyzed", total)

    with c2:
        render_metric_card("Flagged Transactions", anomalies)

    with c3:
        render_metric_card("Transactions Not Flagged", normal)

    st.markdown("")
    st.markdown("## How It Works")
    st.markdown(
        '<p class="subtitle">Three steps to turn transaction data into '
        'actionable insights.</p>',
        unsafe_allow_html=True,
    )

    step1, step2, step3 = st.columns(3)

    with step1:
        st.markdown(
            """
            <div class="step-card">
                <div class="step-number">01</div>
                <div class="step-title">Enter Transaction</div>
                <div class="subtitle">
                    Provide transaction details such as amount, location,
                    merchant category, and usual customer behaviour.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with step2:
        st.markdown(
            """
            <div class="step-card">
                <div class="step-number">02</div>
                <div class="step-title">Detect Anomalies</div>
                <div class="subtitle">
                    The backend evaluates transaction patterns and assigns
                    a risk score based on configured detection rules.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with step3:
        st.markdown(
            """
            <div class="step-card">
                <div class="step-number">03</div>
                <div class="step-title">Understand the Risk</div>
                <div class="subtitle">
                    Review the indicators and the AI-generated explanation
                    returned by the backend.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("")
    st.markdown("## Why BankGuard AI?")

    feature1, feature2 = st.columns(2)

    with feature1:
        st.markdown(
            """
            <div class="panel">
                <div class="panel-title">🔍 Explainable Detection</div>
                <p class="subtitle">
                    Highlight unusual amounts, locations, transaction
                    times, and merchant categories using the backend's
                    anomaly-detection rules.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with feature2:
        st.markdown(
            """
            <div class="panel">
                <div class="panel-title">🧠 AI-Assisted Insights</div>
                <p class="subtitle">
                    Convert technical detection results into a more
                    understandable explanation for human review.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("")
    if st.button("＋ Analyze a Transaction", use_container_width=True):
        st.session_state.page = "Analyze Transaction"
        st.rerun()


# ============================================================
# ANALYZE TRANSACTION PAGE
# ============================================================

elif page == "Analyze Transaction":

    st.title("Analyze Transaction")
    st.markdown(
        '<p class="subtitle">Enter the transaction details below. '
        'BankGuard AI will submit them to your FastAPI backend.</p>',
        unsafe_allow_html=True,
    )

    with st.form("transaction_form", clear_on_submit=False):

        st.markdown("### 🧾 Transaction Information")

        col1, col2 = st.columns(2)

        with col1:
            transaction_id = st.text_input(
                "Transaction ID",
                value=f"TXN{datetime.now().strftime('%Y%m%d%H%M%S')}",
            )

            customer_id = st.text_input(
                "Customer ID",
                value="CUST1001",
            )

            amount = st.number_input(
                "Transaction Amount",
                min_value=0.01,
                value=85000.0,
                step=500.0,
                format="%.2f",
            )

            currency = st.selectbox(
                "Currency",
                ["INR", "USD", "EUR", "GBP"],
            )

        with col2:
            location = st.text_input(
                "Transaction Location",
                value="Bengaluru",
            )

            transaction_type = st.selectbox(
                "Transaction Type",
                [
                    "UPI",
                    "Card Payment",
                    "Bank Transfer",
                    "ATM Withdrawal",
                    "Online Payment",
                    "Other",
                ],
            )

            merchant_category = st.selectbox(
                "Merchant Category",
                [
                    "Groceries",
                    "Food",
                    "Shopping",
                    "Travel",
                    "Utilities",
                    "Electronics",
                    "Jewellery",
                    "Gambling",
                    "Cryptocurrency",
                    "Healthcare",
                    "Other",
                ],
            )

        st.markdown("### 👤 Customer's Usual Behaviour")

        col3, col4 = st.columns(2)

        with col3:
            usual_transaction_amount = st.number_input(
                "Usual Transaction Amount",
                min_value=0.0,
                value=4500.0,
                step=250.0,
                format="%.2f",
                help="The customer's typical transaction amount.",
            )

        with col4:
            usual_location = st.text_input(
                "Usual Transaction Location",
                value="Mysuru",
            )

        st.markdown("### 🕒 Transaction Time")

        transaction_date = st.date_input(
            "Transaction Date",
            value=datetime.now().date(),
        )

        transaction_time = st.time_input(
            "Transaction Time",
            value=datetime.now().time().replace(microsecond=0),
        )

        submitted = st.form_submit_button(
            "🔍 Analyze Transaction",
            use_container_width=True,
        )

    if submitted:
        if not transaction_id.strip():
            st.error("Please enter a transaction ID.")

        elif not customer_id.strip():
            st.error("Please enter a customer ID.")

        elif not location.strip():
            st.error("Please enter the transaction location.")

        elif not usual_location.strip():
            st.error("Please enter the customer's usual location.")

        else:
            timestamp = datetime.combine(
                transaction_date,
                transaction_time,
            ).isoformat(timespec="seconds")

            payload = {
                "transaction_id": transaction_id.strip(),
                "customer_id": customer_id.strip(),
                "amount": float(amount),
                "currency": currency,
                "location": location.strip(),
                "transaction_time": timestamp,
                "transaction_type": transaction_type,
                "merchant_category": merchant_category,
                "usual_transaction_amount": float(
                    usual_transaction_amount
                ),
                "usual_location": usual_location.strip(),
            }

            with st.spinner(
                "Analyzing transaction and generating explanation..."
            ):
                result = analyze_transaction(payload)

            if result:
                st.success("Transaction analysis completed.")
                render_result(result)

    if (
        st.session_state.last_result
        and not submitted
    ):
        st.markdown("---")
        st.markdown("### Previous Analysis")

        if st.button("Show Last Analysis"):
            render_result(st.session_state.last_result)


# ============================================================
# TRANSACTION HISTORY PAGE
# ============================================================

elif page == "Transaction History":

    st.title("Transaction History")
    st.markdown(
        '<p class="subtitle">Review the transactions analyzed during '
        'this application session.</p>',
        unsafe_allow_html=True,
    )

    history = st.session_state.history

    if not history:
        st.info(
            "No transactions have been analyzed yet. "
            "Open Analyze Transaction to get started."
        )

    else:
        total = len(history)
        anomalies = sum(
            get_anomaly_status(item)
            for item in history
        )

        c1, c2, c3 = st.columns(3)

        with c1:
            render_metric_card("Total", total)

        with c2:
            render_metric_card("Flagged", anomalies)

        with c3:
            render_metric_card("Not Flagged", total - anomalies)

        st.markdown("")

        rows = []

        for item in history:
            score = normalize_risk_score(
                item.get("risk_score", item.get("risk", 0))
            )

            rows.append({
                "Transaction ID": mask_id(item.get("transaction_id", "N/A")),
                "Customer ID": mask_id(item.get("customer_id", "N/A")),
                "Amount": money(
                    item.get("amount", 0),
                    item.get("currency", "INR"),
                ),
                "Location": item.get("location", "N/A"),
                "Status": (
                    "⚠️ Flagged"
                    if get_anomaly_status(item)
                    else "✓ Not flagged"
                ),
                "Risk Score": f"{score:.1f}%",
                "Analyzed At": item.get("_analyzed_at", "N/A"),
            })

        st.dataframe(
            rows,
            use_container_width=True,
            hide_index=True,
        )

        search_id = st.text_input(
            "Search by Transaction ID",
            placeholder="Enter a transaction ID...",
        )

        filtered_history = history

        if search_id.strip():
            filtered_history = [
                item
                for item in history
                if search_id.strip().lower()
                in str(item.get("transaction_id", "")).lower()
            ]

        st.markdown("### Transaction Details")

        if not filtered_history:
            st.warning("No matching transactions found.")

        else:
            options = [
                (
                    f"{mask_id(item.get('transaction_id', 'N/A'))} — "
                    f"{'Flagged' if get_anomaly_status(item) else 'Not flagged'}"
                )
                for item in filtered_history
            ]

            selected_label = st.selectbox(
                "Choose a transaction",
                options,
            )

            selected_index = options.index(selected_label)
            selected_item = filtered_history[selected_index]

            st.markdown('<div class="panel">', unsafe_allow_html=True)

            st.write(
                "**Transaction ID:**",
                mask_id(selected_item.get("transaction_id", "N/A")),
            )
            st.write(
                "**Customer ID:**",
                mask_id(selected_item.get("customer_id", "N/A")),
            )
            st.write(
                "**Amount:**",
                money(
                    selected_item.get("amount", 0),
                    selected_item.get("currency", "INR"),
                ),
            )
            st.write(
                "**Location:**",
                selected_item.get("location", "N/A"),
            )
            st.write(
                "**Transaction Time:**",
                selected_item.get("transaction_time", "N/A"),
            )
            st.write(
                "**Status:**",
                "Flagged" if get_anomaly_status(selected_item)
                else "Not flagged",
            )
            st.write("**Explanation:**", get_explanation(selected_item))

            st.markdown("</div>", unsafe_allow_html=True)

            with st.expander("View complete analysis"):
                display_item = {
                    key: value
                    for key, value in selected_item.items()
                    if not key.startswith("_")
                }

                if "transaction_id" in display_item:
                    display_item["transaction_id"] = mask_id(
                        display_item["transaction_id"]
                    )

                if "customer_id" in display_item:
                    display_item["customer_id"] = mask_id(
                        display_item["customer_id"]
                    )

                st.json(display_item)


        st.markdown("---")

        export_data = [
            {
                key: value
                for key, value in item.items()
                if not key.startswith("_")
            }
            for item in history
        ]

        st.download_button(
            "⬇️ Export History as JSON",
            data=json.dumps(
                export_data,
                indent=2,
                ensure_ascii=False,
            ),
            file_name="bankguard_transaction_history.json",
            mime="application/json",
            use_container_width=True,
        )

        if st.button(
            "Clear Session History",
            type="secondary",
            use_container_width=True,
        ):
            st.session_state.history = []
            st.session_state.last_result = None
            st.rerun()

        st.caption(
            "History is stored in the current Streamlit session. "
            "It is not persistent database storage."
        )


# ============================================================
# ABOUT PROJECT PAGE
# ============================================================

elif page == "About Project":

    st.title("About BankGuard AI")

    st.markdown(
        """
        <div class="hero">
            <div class="eyebrow">PROJECT OVERVIEW</div>
            <h1>Making Transaction Risks Easier to Understand</h1>
            <p>
                BankGuard AI is a banking transaction anomaly detection
                and explanation application. It combines rule-based
                detection with AI-assisted explanations to help people
                understand why a transaction may require additional review.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("## Core Features")

    st.markdown(
        """
        <div class="panel">
            <div class="panel-title">🔍 Anomaly Detection</div>
            <p class="subtitle">
                Evaluates transaction information using the backend's
                configured detection rules.
            </p>
        </div>

        <div class="panel">
            <div class="panel-title">📊 Risk Scoring</div>
            <p class="subtitle">
                Presents the risk score returned by the backend as an
                easy-to-read percentage.
            </p>
        </div>

        <div class="panel">
            <div class="panel-title">🧠 AI-Assisted Explanation</div>
            <p class="subtitle">
                Displays the explanation generated by the backend's
                language-model integration, when available.
            </p>
        </div>

        <div class="panel">
            <div class="panel-title">📜 Transaction History</div>
            <p class="subtitle">
                Allows users to review analyses from the current session
                and export them as JSON.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("## Technology Stack")

    tech1, tech2, tech3 = st.columns(3)

    with tech1:
        st.markdown(
            """
            <div class="step-card">
                <div class="step-title">Frontend</div>
                <p class="subtitle">Python · Streamlit</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with tech2:
        st.markdown(
            """
            <div class="step-card">
                <div class="step-title">Backend</div>
                <p class="subtitle">Python · FastAPI</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with tech3:
        st.markdown(
            """
            <div class="step-card">
                <div class="step-title">AI Integration</div>
                <p class="subtitle">Ollama · Local language model</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("")
    st.markdown("## Important Note")

    st.info(
        "BankGuard AI is a prototype for anomaly detection and "
        "explanation. A flagged transaction is not necessarily fraudulent. "
        "Production use would require secure authentication, appropriate "
        "data protection, persistent storage, monitoring, and human review."
    )


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div class="footer">
        🛡️ BankGuard AI · Intelligent Transaction Security<br>
        AI-assisted anomaly detection for human review
    </div>
    """,
    unsafe_allow_html=True,
)
