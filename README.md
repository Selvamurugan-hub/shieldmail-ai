# 🛡️ ShieldMail AI
### Explainable Phishing & Suspicious Message Detection

**Detect suspicious messages. Understand the risks. Make safer decisions.**

ShieldMail AI is a web-based cybersecurity tool that analyzes emails and text messages for potential phishing attempts, social engineering, suspicious links, credential theft, and urgency-based manipulation. It combines a React frontend with a FastAPI backend to deliver risk scores, explainable findings, and actionable safety recommendations.

Built for **ForgeHacks Online 2026 — AI + Cybersecurity**.

---

## 🚨 The Problem

Phishing messages often imitate trusted organizations, create a sense of urgency, and trick people into revealing passwords, financial information, or other sensitive data.

Traditional users may struggle to identify warning signs, especially when a message looks convincing.

ShieldMail AI aims to make suspicious-message analysis more accessible by explaining **what looks suspicious, why it matters, and what the user should do next.**

## 💡 Our Solution

ShieldMail AI analyzes user-submitted message text and generates an explainable security assessment.

### Key Features

- **🔍 Message Analysis** — Analyze pasted email or message content for suspicious patterns.
- **📊 Risk Scoring** — Generate a risk score and risk category based on detected indicators.
- **🧠 Explainable Findings** — Show detected warning signs, their descriptions, and associated risk contributions.
- **🎯 Threat Indicators** — Identify patterns associated with urgency, credential requests, and suspicious messaging.
- **🛡️ Safety Recommendations** — Provide practical next steps based on the analysis.
- **📚 Analysis History** — Review previous analyses saved in the browser, if enabled in the frontend.
- **📤 Export Results** — Export analysis results as JSON, if supported by the current frontend.
- **⚡ Interactive Web Interface** — A React-based interface connected to a FastAPI backend.
- **🔌 API Documentation** — Explore and test backend endpoints through Swagger UI.

> **Important:** ShieldMail AI currently uses a rule-based analysis engine. It does not guarantee detection of every phishing message, and its risk score should not be interpreted as a statistically calibrated probability.

---

## 🖥️ Application Workflow

1. **Submit:** Paste a suspicious email or message into the analyzer.
2. **Analyze:** The backend checks the text against supported detection rules.
3. **Identify:** Relevant warning indicators and their risk contributions are collected.
4. **Assess:** The system calculates a risk score and assigns a risk category.
5. **Explain:** The interface presents the findings and recommended safety actions.
6. **Decide:** The user reviews the evidence and independently verifies the message before taking action.

---

## 🏗️ System Architecture

```text
┌──────────────────────────┐
│        User              │
│  Email / Message Text    │
└────────────┬─────────────┘
             │
             ▼
┌──────────────────────────┐
│ React + Vite Frontend    │
│ Input, Results, History  │
└────────────┬─────────────┘
             │ HTTP API
             ▼
┌──────────────────────────┐
│ FastAPI Backend          │
│ Request Validation       │
└────────────┬─────────────┘
             │
             ▼
┌──────────────────────────┐
│ Rule-Based Analysis      │
│ Threat Indicator Checks  │
│ Risk Score & Findings    │
└────────────┬─────────────┘
             │
             ▼
┌──────────────────────────┐
│ Explainable Results      │
│ Risk Level & Guidance    │
└──────────────────────────┘
```

---

## 🧰 Technology Stack

| Layer | Technology |
|---|---|
| Frontend | React |
| Development Server & Build Tool | Vite |
| Frontend Language | JavaScript |
| Backend Framework | FastAPI |
| Backend Language | Python |
| API Server | Uvicorn |
| API Documentation | OpenAPI / Swagger UI |
| Analysis Engine | Rule-based text analysis |
| Version Control | Git & GitHub |

---

## 📂 Project Structure

```text
shieldmail-ai/
├── backend/
│   └── app/
│       └── main.py
├── frontend/
│   ├── public/
│   ├── src/
│   ├── package.json
│   └── vite.config.js
├── tests/
├── .gitignore
└── README.md
```

*The structure above is representative. Additional files and folders may be present in your local project.*

---

## ⚙️ Getting Started

### Prerequisites

Install the following before running the application:

- Python 3.12 or another compatible Python version
- Node.js and npm
- Git

### 1. Clone the Repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd shieldmail-ai
```

Replace `YOUR_GITHUB_REPOSITORY_URL` with your actual GitHub repository URL.

### 2. Set Up the Backend

From the project root, create and activate a Python virtual environment.

**Windows PowerShell:**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install the backend dependencies:

```powershell
pip install -r backend/requirements.txt
```

Start the backend:

```powershell
python -m uvicorn app.main:app --app-dir backend --reload --host 127.0.0.1 --port 8000
```

Backend URL:

```text
http://127.0.0.1:8000
```

Interactive API documentation:

```text
http://127.0.0.1:8000/docs
```

**Note:** The install command assumes `backend/requirements.txt` exists and contains the required dependencies. If your repository does not include that file, add a verified dependency list before following this step.

### 3. Set Up the Frontend

Open a second terminal:

```powershell
cd frontend
npm install
npm run dev
```

Open the local URL printed by Vite, typically:

```text
http://localhost:5173
```

Keep both the backend and frontend running while using the application.

---

## 🔌 API Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| `GET` | `/api/health` | Check backend health and analysis configuration |
| `GET` | `/api/examples` | Retrieve supported example messages |
| `POST` | `/api/analyze` | Analyze submitted message text |

Use the Swagger UI at `/docs` to inspect request schemas, response formats, and available endpoints.

---

## 🧪 Testing

Run the available backend tests from the project root:

```powershell
python -m pytest
```

Make sure your virtual environment is activated and the test dependencies are installed. The command should be run against the tests included in the repository.

---

## 🔐 Security & Privacy

- Analyze only messages you are authorized to inspect.
- Do not submit real passwords, authentication tokens, financial credentials, or other highly sensitive information.
- Treat analysis results as advisory, not definitive security verdicts.
- Do not open suspicious links or attachments merely to verify an analysis.
- Avoid committing `.env` files, API keys, virtual environments, or dependency folders to GitHub.
- Review the backend's logging, storage, and deployment configuration before processing sensitive information.

### Current Limitations

- The current detection engine is rule-based and may produce false positives or false negatives.
- A risk score is a heuristic assessment, not a calibrated probability that a message is malicious.
- Text analysis alone cannot conclusively verify a sender's identity or establish whether a URL or domain is malicious.
- Live domain reputation checks, URL sandboxing, and email-header authentication checks should not be assumed to be available unless implemented and tested.

---

## 🚀 Future Enhancements

- Machine-learning-based phishing classification
- URL and domain reputation analysis
- Email-header and sender-authentication checks
- Detection of spoofing and impersonation patterns
- Multilingual phishing detection
- Confidence estimation and clearer uncertainty reporting
- Downloadable security reports
- Expanded test datasets and evaluation metrics
- Secure deployment and monitoring

These are planned enhancements, not claims about the current implementation.

---

## 🎯 Project Goal

ShieldMail AI aims to make cybersecurity more understandable by combining automated suspicious-message analysis with transparent findings and practical recommendations.

Rather than presenting only a risk label, the project focuses on helping users understand the warning signs behind a potentially dangerous message.

---

## 🤝 Contributing

Contributions, bug reports, and suggestions are welcome.

1. Fork the repository.
2. Create a feature branch.
3. Make and test your changes.
4. Submit a pull request describing the improvement.

---

## ⚠️ Disclaimer

ShieldMail AI is an educational cybersecurity project and decision-support tool. It is not a replacement for professional security tools, incident-response processes, or independent verification. No detection system can guarantee that every phishing attempt will be identified.

---

## 👨‍💻 Built For

**ForgeHacks Online 2026 — AI + Cybersecurity**

*Building more transparent and accessible cybersecurity tools, one message at a time.*

