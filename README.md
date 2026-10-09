# ShieldMail AI
*Detect the deception. Understand the risk. Stay protected.* — ForgeHacks Online 2026, AI + Cybersecurity

**Assistive tool, not a guarantee of scam detection.** Scores are heuristic, not probabilities.

## Status (honest)
- Done: FastAPI backend, deterministic rule engine, 8 synthetic samples, 26 pytest tests.
- Not built yet: React/Vite frontend, Ollama integration, history/export, Devpost text, demo script, screenshots.

## Run (Windows PowerShell)
```powershell
cd shieldmail-ai
py -3.12 -m venv .venv   # or: python -m venv .venv
.\.venv\Scripts\Activate.ps1   # if blocked: Set-ExecutionPolicy -Scope Process Bypass
pip install -r backend\requirements.txt
python -m uvicorn app.main:app --app-dir backend --reload --host 127.0.0.1 --port 8000
```
Swagger docs: http://127.0.0.1:8000/docs. Tests: `cd backend; python -m pytest -q`. Stop with Ctrl+C. Port busy: use `--port 8001`.

## Scoring
Each category counts once (strongest finding carries the points): credential 20, urgency 15, URL 20, impersonation 20, payment 20, reward 10, context 5; +10 when 3+ categories fire; cap 100. Levels: 0–24 Low, 25–49 Medium, 50–74 High, 75–100 Critical. No URL is ever visited; no reputation/WHOIS/DNS checks are made.
