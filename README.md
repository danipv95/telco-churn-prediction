# Telco Churn Prediction

This project is a production-ready data science web app for telecom churn prediction, designed with a modern, unified UI/UX and robust backend architecture. Built for clarity, maintainability, and professional presentation.

## Tech Stack
- **Backend:** Python 3.8+ | FastAPI
- **Frontend:** HTML5 | CSS3 | Vanilla JavaScript | Chart.js
- **Database:** SQLite (dev) | PostgreSQL (production)
- **ML Model:** XGBoost | Feature engineering | Model artifacts in /outputs

## Architecture
```
telco-churn-prediction/
├── app/
│   ├── main.py            # FastAPI app entrypoint
│   ├── utils/             # Data loaders, design system, etc.
│   └── templates/
│       └── index.html     # Main frontend template
├── static/
│   └── css/
│       └── style.css      # Unified design system
├── notebooks/             # Jupyter/Colab notebooks for EDA/modeling
├── src/                   # ML model scripts, feature engineering
├── data/                  # (No raw data in repo)
├── outputs/               # Model artifacts, results
├── README.md
├── requirements.txt
├── .gitignore
└── LICENSE
```

## How to Run
1. Clone the repo and install dependencies:
	```bash
	git clone https://github.com/youruser/telco-churn-prediction.git
	cd telco-churn-prediction
	pip install -r requirements.txt
	```
2. Start the FastAPI server:
	```bash
	uvicorn app.main:app --reload
	```
3. Open [http://localhost:8000](http://localhost:8000) in your browser.

## Deployment
- Recommended: Render.com (free tier)
- Set environment variables securely in Render dashboard
- Do not commit sensitive data or secrets

## Security & Best Practices
- Environment variables for secrets
- .gitignore for sensitive files
- HTTPS recommended for production
- CORS configured for security

## License
MIT

---
Senior Data Analytics Portfolio · Daniel Padilla
# telco-churn-prediction
Customer churn prediction with risk segmentation and intervention recommender — XGBoost, Python, Kaggle
