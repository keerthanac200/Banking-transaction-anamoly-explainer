# 🛡️ BankGuard AI

### AI-Powered Banking Transaction Anomaly Detection & Explanation

**From a randomly selected problem statement to an AI-powered solution.**

BankGuard AI is an AI-powered banking transaction anomaly detection system developed for the **TCS Tech Day AI Hackathon**. It identifies potentially suspicious banking transactions using rule-based detection and risk scoring, then uses a local Large Language Model (LLM) to explain the detected anomalies in simple, understandable language.

Our goal is to help users understand unusual transaction patterns and make informed decisions through clear explanations and suggested actions.

---

## 🚀 Key Features

* **🔍 Anomaly Detection:** Identifies potentially suspicious transactions using predefined detection rules.
* **📊 Risk Scoring:** Calculates a risk score based on the detected anomalies.
* **🤖 AI-Powered Explanations:** Uses Gemma 3 through Ollama to explain why a transaction may be suspicious.
* **💡 Suggested Actions:** Provides recommendations based on the detected transaction patterns.
* **🌍 Location Analysis:** Flags transactions made from locations different from the customer's usual location.
* **💰 High-Amount Detection:** Identifies transactions that significantly exceed the customer's usual transaction amount.
* **🕒 Unusual-Time Detection:** Flags transactions made during unusual hours.
* **🏪 Merchant Category Detection:** Flags transactions involving selected high-risk merchant categories.
* **📋 Transaction History:** Supports reviewing transaction information and analysis results.
* **🔒 Privacy-Conscious Design:** Uses local AI inference and can mask sensitive identifiers in the interface.

## 🧠 How It Works

1. **Transaction Input:** The system receives banking transaction details.
2. **Rule-Based Analysis:** The anomaly detection engine evaluates the transaction against predefined rules.
3. **Risk Score Calculation:** The system calculates a score based on the detected anomalies.
4. **AI Explanation:** Gemma 3 generates a human-readable explanation using the transaction details and analysis results.
5. **Suggested Action:** The system presents the risk level and a suggested next step.
6. **Result Display:** The user can review the analysis through the application interface.

## 🧪 Anomaly Detection Rules

BankGuard AI evaluates transactions using the following rules:

| Rule                      | Description                                                                           |
| ------------------------- | ------------------------------------------------------------------------------------- |
| High Amount               | Flags transactions exceeding five times the customer's usual transaction amount.      |
| Unusual Location          | Flags transactions made from a location different from the customer's usual location. |
| Unusual Time              | Flags transactions made before 6:00 AM or at or after 11:00 PM.                       |
| Unusual Merchant Category | Flags selected categories such as jewellery, gambling, and cryptocurrency.            |

Each triggered rule contributes to the transaction's risk score. The system combines the results and caps the score at `0.99`.

**Important:** A flagged transaction is not necessarily fraudulent. The system identifies patterns that may warrant further review.

## 🛠️ Technology Stack

| Technology   | Purpose                                            |
| ------------ | -------------------------------------------------- |
| Python       | Core application logic                             |
| FastAPI      | Backend API development                            |
| Streamlit    | Web interface, where configured                    |
| Ollama       | Local LLM execution                                |
| Gemma 3 (4B) | AI-powered transaction explanations                |
| JSON         | Transaction sample data and structured information |
| Git & GitHub | Version control and collaboration                  |

## 📂 Project Structure

```text
BankGuard-AI/
│
├── app/
│   ├── app.py
│   ├── anomaly_engine.py
│   └── llm_explainer.py
│
├── data/
│   └── transactions.json
│
├── .gitignore
└── README.md
```

*Note: Update this structure if your latest repository contains additional frontend files, configuration files, or folders.*

## ⚙️ Installation and Setup

### Prerequisites

Install the following:

* Python 3.12
* Git
* Ollama
* Gemma 3 (4B) model

### 1. Clone the Repository

```bash
git clone https://github.com/keerthanac200/Banking-transaction-anamoly-explainer.git
cd Banking-transaction-anamoly-explainer
```

### 2. Create a Virtual Environment

On Windows PowerShell:

```powershell
py -3.12 -m venv .venv
```

Activate the environment:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 3. Install Dependencies

```powershell
python -m pip install fastapi "uvicorn[standard]" pydantic requests streamlit
```

### 4. Set Up the AI Model

Install Ollama and download the model:

```powershell
ollama pull gemma3:4b
```

Ensure Ollama is running before testing AI-generated explanations.

### 5. Start the Backend

From the project root:

```powershell
python -m uvicorn app.app:app --reload
```

The FastAPI server should start on:

```text
http://127.0.0.1:8000
```

To access the interactive API documentation, open:

```text
http://127.0.0.1:8000/docs
```

The backend includes a health/root endpoint (`GET /`) and a transaction analysis endpoint (`POST /analyze`).

### 6. Run the Frontend

If your current Streamlit frontend entry point is `frontend/app.py`, open a second terminal and run:

```powershell
python -m streamlit run frontend/app.py
```

Use the frontend entry point that matches your latest repository structure.

## 🎯 Example Use Case

Consider a transaction with these details:

* **Transaction ID:** TXN1001
* **Transaction Amount:** ₹85,000
* **Customer's Usual Transaction Amount:** ₹4,500
* **Transaction Location:** Bengaluru
* **Customer's Usual Location:** Mysuru
* **Transaction Time:** 2:13 AM

The system may flag the transaction for:

* High transaction amount
* Unusual location
* Unusual transaction time

The rule-based engine calculates the risk score, and the AI model generates an explanation to help the user understand why the transaction was flagged.

*This is an illustrative example, not proof of fraudulent activity.*

## 🏆 Hackathon Journey

BankGuard AI was developed as part of the **TCS Tech Day AI Hackathon**.

Our team began with a randomly selected problem statement, divided responsibilities, and collaborated to develop a solution combining rule-based anomaly detection with AI-generated explanations.

The project helped us explore backend development, API integration, local language models, anomaly detection, and collaborative software development.

## 👩‍💻 Contributors

Developed by students from **Dr. Ambedkar Institute of Technology**.

| No. | Contributor    |
| --: | -------------- |
|   1 | Keerthana C    |
|   2 | Aishwarya C    |
|   3 | Supriya J K    |
|   4 | Dhanushree B S |
|   5 | Akula Bhuvana  |

## 🔮 Future Enhancements

* Integrate more advanced anomaly detection techniques.
* Add configurable detection rules and risk thresholds.
* Improve AI explanations and suggested actions.
* Add transaction filtering, search, and downloadable reports.
* Explore real-time transaction monitoring.
* Evaluate detection accuracy using larger, representative datasets.
* Strengthen security, authentication, and data protection.

## ⚠️ Disclaimer

BankGuard AI is an educational and hackathon project. Its results are intended to support transaction review, not replace professional fraud investigation or a bank's security systems. The system may produce false positives or miss suspicious transactions. Never rely on an AI-generated explanation alone to determine whether a transaction is fraudulent.

## ⭐ Acknowledgements

We thank **TCS Tech Day AI Hackathon** for the opportunity to explore AI-driven problem-solving and build a practical project collaboratively.

If you find this project interesting, consider giving the repository a ⭐ on GitHub!
