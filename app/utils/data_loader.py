import pandas as pd
import numpy as np
from pathlib import Path
from sklearn.metrics import roc_auc_score

# ── Paths ──────────────────────────────────────────────────────────────────────
BASE_DIR       = Path(__file__).resolve().parent.parent.parent
DATA_DIR       = BASE_DIR / "data"
DASHBOARD_PATH = DATA_DIR / "dashboard_data.csv"
OOF_PATH       = DATA_DIR / "oof_predictions.csv"

# ── Risk config ────────────────────────────────────────────────────────────────
RISK_COLORS = {
    'Low'     : '#2ecc71',
    'Medium'  : '#f39c12',
    'High'    : '#e74c3c',
    'Critical': '#8e44ad',
}
RISK_ORDER = ['Low', 'Medium', 'High', 'Critical']

# ── Loaders ────────────────────────────────────────────────────────────────────
def load_all():
    dashboard = pd.read_csv(DASHBOARD_PATH)
    dashboard['risk_level'] = pd.Categorical(
        dashboard['risk_level'], categories=RISK_ORDER, ordered=True
    )
    oof = pd.read_csv(OOF_PATH)
    return dashboard, oof

# ── KPIs ───────────────────────────────────────────────────────────────────────
def get_kpis(df: pd.DataFrame, oof: pd.DataFrame) -> dict:
    total     = len(df)
    at_risk   = len(df[df['churn_probability'] >= 0.25])
    high_risk = len(df[df['churn_probability'] >= 0.50])
    critical  = len(df[df['churn_probability'] >= 0.75])
    avg_prob  = df['churn_probability'].mean()
    oof_auc   = roc_auc_score(oof['Churn_real'], oof['Churn_pred'])

    return {
        'total'        : total,
        'at_risk'      : at_risk,
        'high_risk'    : high_risk,
        'critical'     : critical,
        'avg_prob'     : avg_prob,
        'oof_auc'      : oof_auc,
        'at_risk_pct'  : at_risk   / total * 100,
        'high_risk_pct': high_risk / total * 100,
    }