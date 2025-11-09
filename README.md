# Flight Fare & Sentiment Analyzer

Project scaffold for Flight Fare & Sentiment Analyzer (MERN + Python NLP + LLM)

Quick start (local development):

1) Backend
```
cd backend
npm install
npm run dev
```

2) Scraper & NLP
```
cd scraper_nlp
python -m venv .venv
# On Windows PowerShell
.\.venv\Scripts\Activate.ps1; pip install -r requirements.txt
python main.py
```

3) Frontend
```
cd frontend
npm install
npm run dev
```

See `backend/.env.example` and `scraper_nlp/requirements.txt` for environment variables and dependencies.

Deployment guide is in `backend/DEPLOYMENT.md` and `frontend/DEPLOYMENT.md`.
