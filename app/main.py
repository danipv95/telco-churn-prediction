import streamlit as st
import sys
from pathlib import Path
import pandas as pd
import numpy as np
from streamlit_echarts import st_echarts
import plotly.graph_objects as go
from sklearn.metrics import roc_curve, roc_auc_score, confusion_matrix

sys.path.append(str(Path(__file__).resolve().parent))
from utils.data_loader import load_all, get_kpis, RISK_COLORS
from utils.insights import (
    get_overview_insights, get_contract_insight, get_internet_insight,
    get_payment_insight, get_tenure_insight, get_customer_risk_insight,
    get_model_insight
)

st.set_page_config(
    page_title="Telco Churn Intelligence",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

*, html, body { font-family: 'Inter', sans-serif !important; box-sizing: border-box; }

/* ── App background ── */
[data-testid="stAppViewContainer"],
[data-testid="stMain"],
.main { background-color: #FFFFFF !important; }
.block-container { padding: 2rem 2.5rem 2rem 2.5rem !important; max-width: 1300px !important; }

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background-color: #1a2744 !important;
    padding: 1.5rem 1rem !important;
}
[data-testid="stSidebar"] section { padding: 0 !important; }
[data-testid="stSidebar"] * { color: #FFFFFF !important; }
[data-testid="stSidebar"] hr { border-color: rgba(255,255,255,0.12) !important; margin: 1rem 0 !important; }
[data-testid="stSidebar"] .stRadio > label { display: none; }
[data-testid="stSidebar"] .stRadio > div { gap: 4px !important; }
[data-testid="stSidebar"] .stRadio label {
    background: rgba(255,255,255,0.06) !important;
    border-radius: 8px !important;
    padding: 10px 14px !important;
    font-size: 0.88rem !important;
    font-weight: 500 !important;
    cursor: pointer !important;
    transition: background 0.15s !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
}
[data-testid="stSidebar"] .stRadio label:hover {
    background: rgba(255,255,255,0.12) !important;
}
[data-testid="stSidebar"] .stMultiSelect label,
[data-testid="stSidebar"] .stSlider label {
    font-size: 0.78rem !important;
    text-transform: uppercase !important;
    letter-spacing: 0.8px !important;
    color: rgba(255,255,255,0.6) !important;
    margin-bottom: 4px !important;
}
[data-testid="stSidebar"] .stMultiSelect [data-baseweb="select"] > div {
    background: rgba(255,255,255,0.08) !important;
    border: 1px solid rgba(255,255,255,0.15) !important;
    border-radius: 6px !important;
}

/* ── Page header ── */
.page-header {
    margin-bottom: 1.5rem;
    padding-bottom: 1rem;
    border-bottom: 1px solid #f0f0f0;
}
.page-title {
    font-size: 1.6rem;
    font-weight: 700;
    color: #1a2744;
    margin: 0 0 4px 0;
    line-height: 1.2;
}
.page-subtitle {
    font-size: 0.88rem;
    color: #8492a6;
    margin: 0;
}

/* ── KPI Cards ── */
.kpi-card {
    background: #FFFFFF;
    border: 1px solid #e8ecf0;
    border-radius: 12px;
    padding: 18px 20px 14px 20px;
    position: relative;
    overflow: hidden;
}
.kpi-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0;
    width: 3px; height: 100%;
    background: #1a2744;
    border-radius: 12px 0 0 12px;
}
.kpi-label {
    font-size: 0.7rem;
    font-weight: 600;
    color: #8492a6;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin: 0 0 8px 0;
}
.kpi-value {
    font-size: 1.85rem;
    font-weight: 700;
    color: #1a2744;
    margin: 0 0 4px 0;
    line-height: 1;
}
.kpi-delta {
    font-size: 0.78rem;
    color: #8492a6;
    margin: 0;
    font-weight: 400;
}

/* ── Section cards ── */
.section-card {
    background: #FFFFFF;
    border: 1px solid #e8ecf0;
    border-radius: 12px;
    padding: 20px 22px 16px 22px;
    margin-bottom: 16px;
}
.section-title {
    font-size: 0.92rem;
    font-weight: 700;
    color: #1a2744;
    margin: 0 0 2px 0;
}
.section-desc {
    font-size: 0.78rem;
    color: #8492a6;
    margin: 0 0 14px 0;
}

/* ── Insight box ── */
.insight {
    background: #fffbf5;
    border-left: 3px solid #FF8C00;
    border-radius: 0 6px 6px 0;
    padding: 10px 14px;
    margin-top: 12px;
    font-size: 0.82rem;
    color: #374151;
    line-height: 1.55;
}

/* ── Divider ── */
.divider { height: 1px; background: #f0f0f0; margin: 20px 0; }

/* ── Table ── */
div[data-testid="stDataFrame"] {
    border: 1px solid #e8ecf0 !important;
    border-radius: 8px !important;
    overflow: hidden !important;
}

/* ── Download button ── */
.stDownloadButton button {
    background: #1a2744 !important;
    color: white !important;
    border: none !important;
    border-radius: 6px !important;
    font-size: 0.82rem !important;
    padding: 6px 16px !important;
    font-weight: 500 !important;
}

/* ── Hide branding ── */
#MainMenu, footer, header { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# ── Data ──────────────────────────────────────────────────────────────────────
@st.cache_data
def get_data():
    return load_all()

dashboard, oof = get_data()
kpis = get_kpis(dashboard, oof)

ECHART_BG = "transparent"

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='margin-bottom:1.5rem'>
        <div style='font-size:0.7rem;font-weight:600;text-transform:uppercase;letter-spacing:1px;color:rgba(255,255,255,0.5);margin-bottom:4px'>Product</div>
        <div style='font-size:1.1rem;font-weight:700;color:#FFFFFF'>Telco Churn</div>
        <div style='font-size:0.82rem;color:rgba(255,255,255,0.6)'>Intelligence Dashboard</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='font-size:0.7rem;font-weight:600;text-transform:uppercase;letter-spacing:1px;color:rgba(255,255,255,0.4);margin-bottom:8px'>Navigation</div>", unsafe_allow_html=True)

    page = st.radio("", ["Overview", "Customer Risk", "Model Performance", "Business Insights"])

    st.markdown("---")

    st.markdown("<div style='font-size:0.7rem;font-weight:600;text-transform:uppercase;letter-spacing:1px;color:rgba(255,255,255,0.4);margin-bottom:10px'>Model Info</div>", unsafe_allow_html=True)
    st.markdown(f"""
    <div style='display:flex;flex-direction:column;gap:8px'>
        <div style='display:flex;justify-content:space-between;font-size:0.82rem'>
            <span style='color:rgba(255,255,255,0.55)'>Algorithm</span>
            <span style='color:#FFFFFF;font-weight:500'>XGBoost</span>
        </div>
        <div style='display:flex;justify-content:space-between;font-size:0.82rem'>
            <span style='color:rgba(255,255,255,0.55)'>Validation</span>
            <span style='color:#FFFFFF;font-weight:500'>10-Fold CV</span>
        </div>
        <div style='display:flex;justify-content:space-between;font-size:0.82rem'>
            <span style='color:rgba(255,255,255,0.55)'>OOF AUC</span>
            <span style='color:#FF8C00;font-weight:700'>{kpis['oof_auc']:.3f}</span>
        </div>
        <div style='display:flex;justify-content:space-between;font-size:0.82rem'>
            <span style='color:rgba(255,255,255,0.55)'>Customers</span>
            <span style='color:#FFFFFF;font-weight:500'>{kpis['total']:,}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("<div style='font-size:0.72rem;color:rgba(255,255,255,0.3);line-height:1.5'>Telco Churn Prediction v1.0<br>Daniel Padilla — 2026</div>", unsafe_allow_html=True)

# ── Helper: KPI card ──────────────────────────────────────────────────────────
def kpi(label, value, delta="", color="#1a2744", accent="#1a2744"):
    return f"""<div class="kpi-card" style="border-left: none">
        <div style="position:absolute;top:0;left:0;width:3px;height:100%;background:{accent};border-radius:12px 0 0 12px"></div>
        <p class="kpi-label">{label}</p>
        <p class="kpi-value" style="color:{color}">{value}</p>
        <p class="kpi-delta">{delta}</p>
    </div>"""

# =============================================================================
# PAGE 1 — OVERVIEW
# =============================================================================
if page == "Overview":
    st.markdown("""<div class="page-header">
        <p class="page-title">Churn Intelligence Overview</p>
        <p class="page-subtitle">How many customers are at risk — and how urgent is it?</p>
    </div>""", unsafe_allow_html=True)

    c1, c2, c3, c4, c5 = st.columns(5)
    with c1: st.markdown(kpi("Total Customers", f"{kpis['total']:,}", "Test set"), unsafe_allow_html=True)
    with c2: st.markdown(kpi("At Risk", f"{kpis['at_risk']:,}", f"{kpis['at_risk_pct']:.1f}% — prob ≥25%", "#f39c12", "#f39c12"), unsafe_allow_html=True)
    with c3: st.markdown(kpi("High Risk", f"{kpis['high_risk']:,}", f"{kpis['high_risk_pct']:.1f}% — prob ≥50%", "#e74c3c", "#e74c3c"), unsafe_allow_html=True)
    with c4: st.markdown(kpi("Critical", f"{kpis['critical']:,}", "prob ≥75%", "#8e44ad", "#8e44ad"), unsafe_allow_html=True)
    with c5: st.markdown(kpi("Model AUC", f"{kpis['oof_auc']:.3f}", "Out-of-Fold", "#FF8C00", "#FF8C00"), unsafe_allow_html=True)

    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

    col_l, col_r = st.columns(2)

    with col_l:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown('<p class="section-title">Churn Risk Distribution</p>', unsafe_allow_html=True)
        st.markdown('<p class="section-desc">How is predicted churn probability distributed across customers?</p>', unsafe_allow_html=True)
        hist_data, bin_edges = np.histogram(dashboard['churn_probability'], bins=40)
        bin_centers = [(bin_edges[i] + bin_edges[i+1])/2 for i in range(len(bin_edges)-1)]
        st_echarts({
            "backgroundColor": ECHART_BG,
            "tooltip": {"trigger": "axis", "axisPointer": {"type": "shadow"}},
            "xAxis": {"type": "category", "data": [f"{x:.2f}" for x in bin_centers],
                      "axisLabel": {"interval": 7, "fontSize": 10, "color": "#8492a6"},
                      "axisLine": {"lineStyle": {"color": "#e8ecf0"}},
                      "name": "Churn Probability", "nameLocation": "middle", "nameGap": 28,
                      "nameTextStyle": {"color": "#8492a6", "fontSize": 11}},
            "yAxis": {"type": "value", "axisLabel": {"color": "#8492a6", "fontSize": 10},
                      "splitLine": {"lineStyle": {"color": "#f5f5f5"}},
                      "name": "Customers", "nameLocation": "middle", "nameGap": 38,
                      "nameTextStyle": {"color": "#8492a6", "fontSize": 11}},
            "series": [{"type": "bar", "data": hist_data.tolist(),
                        "itemStyle": {"color": "#1a2744", "borderRadius": [3, 3, 0, 0]}}],
            "grid": {"left": "12%", "right": "4%", "bottom": "16%", "top": "4%"}
        }, height="280px")
        st.markdown(f'<div class="insight">{get_overview_insights(dashboard, kpis)}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col_r:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown('<p class="section-title">Customers by Risk Level</p>', unsafe_allow_html=True)
        st.markdown('<p class="section-desc">How many customers fall into each risk segment?</p>', unsafe_allow_html=True)
        risk_counts = dashboard['risk_level'].value_counts().reindex(['Low', 'Medium', 'High', 'Critical']).fillna(0)
        st_echarts({
            "backgroundColor": ECHART_BG,
            "tooltip": {"trigger": "item", "formatter": "{b}: {c} customers ({d}%)"},
            "legend": {"orient": "horizontal", "bottom": "0%", "textStyle": {"fontSize": 11, "color": "#374151"}},
            "series": [{"type": "pie", "radius": ["42%", "68%"], "center": ["50%", "44%"],
                "data": [{"value": int(v), "name": k, "itemStyle": {"color": RISK_COLORS[k]}}
                         for k, v in zip(risk_counts.index, risk_counts.values)],
                "label": {"show": True, "formatter": "{b}: {c}", "fontSize": 11, "color": "#374151"},
                "emphasis": {"itemStyle": {"shadowBlur": 8, "shadowColor": "rgba(0,0,0,0.2)"}}}]
        }, height="280px")
        high_critical = int(risk_counts.get('High', 0)) + int(risk_counts.get('Critical', 0))
        st.markdown(f'<div class="insight"><b>{high_critical} customers</b> require proactive retention (High + Critical). They represent <b>{high_critical/kpis["total"]:.1%}</b> of the base — prioritize these for immediate outreach.</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<p class="section-title">Top 10 Highest Risk Customers</p>', unsafe_allow_html=True)
    st.markdown('<p class="section-desc">Customers with the highest predicted churn probability — prioritize these for retention</p>', unsafe_allow_html=True)
    top10 = dashboard.nlargest(10, 'churn_probability')[
        ['id', 'churn_probability', 'risk_level', 'Contract', 'Tenure', 'MonthlyCharges', 'TotalCharges', 'InternetService', 'PaymentMethod']
    ].copy()
    top10['churn_probability'] = top10['churn_probability'].apply(lambda x: f'{x:.1%}')
    top10['MonthlyCharges'] = top10['MonthlyCharges'].apply(lambda x: f'${x:.2f}')
    top10['TotalCharges'] = top10['TotalCharges'].apply(lambda x: f'${x:.2f}')
    st.dataframe(top10, use_container_width=True, hide_index=True)
    st.markdown('</div>', unsafe_allow_html=True)

# =============================================================================
# PAGE 2 — CUSTOMER RISK
# =============================================================================
elif page == "Customer Risk":
    st.markdown("""<div class="page-header">
        <p class="page-title">Customer Risk Explorer</p>
        <p class="page-subtitle">Filter and explore individual customer churn risk profiles</p>
    </div>""", unsafe_allow_html=True)

    with st.sidebar:
        st.markdown("---")
        st.markdown("<div style='font-size:0.7rem;font-weight:600;text-transform:uppercase;letter-spacing:1px;color:rgba(255,255,255,0.4);margin-bottom:10px'>Filters</div>", unsafe_allow_html=True)
        risk_filter     = st.multiselect("Risk Level", ['Low', 'Medium', 'High', 'Critical'], default=['Medium', 'High', 'Critical'])
        contract_filter = st.multiselect("Contract", sorted(dashboard['Contract'].unique()), default=sorted(dashboard['Contract'].unique()))
        internet_filter = st.multiselect("Internet Service", sorted(dashboard['InternetService'].unique()), default=sorted(dashboard['InternetService'].unique()))
        prob_threshold  = st.slider("Min Probability", 0.0, 1.0, 0.25, 0.05)

    filtered = dashboard[
        (dashboard['risk_level'].isin(risk_filter)) &
        (dashboard['Contract'].isin(contract_filter)) &
        (dashboard['InternetService'].isin(internet_filter)) &
        (dashboard['churn_probability'] >= prob_threshold)
    ].copy()

    c1, c2, c3 = st.columns(3)
    avg_prob = filtered['churn_probability'].mean() if len(filtered) > 0 else 0
    avg_mc   = filtered['MonthlyCharges'].mean() if len(filtered) > 0 else 0
    with c1: st.markdown(kpi("Filtered Customers", f"{len(filtered):,}", f"{len(filtered)/kpis['total']:.1%} of total"), unsafe_allow_html=True)
    with c2: st.markdown(kpi("Avg Churn Probability", f"{avg_prob:.1%}", "Selected segment", "#e74c3c", "#e74c3c"), unsafe_allow_html=True)
    with c3: st.markdown(kpi("Avg Monthly Charges", f"${avg_mc:.2f}", "Selected segment", "#FF8C00", "#FF8C00"), unsafe_allow_html=True)

    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown(f'<div class="insight">{get_customer_risk_insight(filtered, dashboard)}</div>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    display_cols = ['id', 'churn_probability', 'risk_level', 'Contract', 'Tenure',
                    'MonthlyCharges', 'TotalCharges', 'InternetService', 'PaymentMethod',
                    'Gender', 'SeniorCitizen', 'Partner', 'Dependents']
    display_cols = [c for c in display_cols if c in filtered.columns]
    fd = filtered[display_cols].copy().sort_values('churn_probability', ascending=False)
    fd['churn_probability'] = fd['churn_probability'].apply(lambda x: f'{x:.1%}')
    fd['MonthlyCharges']    = fd['MonthlyCharges'].apply(lambda x: f'${x:.2f}')
    st.dataframe(fd, use_container_width=True, hide_index=True, height=480)
    st.download_button("Export to CSV", filtered[display_cols].to_csv(index=False), "churn_risk.csv", "text/csv")
    st.markdown('</div>', unsafe_allow_html=True)

# =============================================================================
# PAGE 3 — MODEL PERFORMANCE
# =============================================================================
elif page == "Model Performance":
    st.markdown("""<div class="page-header">
        <p class="page-title">Model Performance</p>
        <p class="page-subtitle">XGBoost 10-Fold Stratified CV — honest OOF evaluation with no data leakage</p>
    </div>""", unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    with c1: st.markdown(kpi("OOF AUC", f"{kpis['oof_auc']:.4f}", "No leakage", "#FF8C00", "#FF8C00"), unsafe_allow_html=True)
    with c2: st.markdown(kpi("Algorithm", "XGBoost", "Gradient Boosting"), unsafe_allow_html=True)
    with c3: st.markdown(kpi("CV Folds", "10", "Stratified"), unsafe_allow_html=True)
    with c4: st.markdown(kpi("Train Samples", f"{len(oof):,}", "+ 7,043 original"), unsafe_allow_html=True)

    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
    st.markdown(f'<div class="insight" style="margin-bottom:16px">{get_model_insight(kpis["oof_auc"])}</div>', unsafe_allow_html=True)

    col_l, col_r = st.columns(2)

    with col_l:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown('<p class="section-title">OOF Predictions Distribution</p>', unsafe_allow_html=True)
        st.markdown('<p class="section-desc">How well does the model separate churners from non-churners?</p>', unsafe_allow_html=True)
        cp  = oof[oof['Churn_real'] == 1]['Churn_pred'].values
        ncp = oof[oof['Churn_real'] == 0]['Churn_pred'].values
        hc,  ec  = np.histogram(cp,  bins=40, range=(0,1))
        hnc, enc = np.histogram(ncp, bins=40, range=(0,1))
        ctr = [(ec[i]+ec[i+1])/2 for i in range(len(ec)-1)]
        st_echarts({
            "backgroundColor": ECHART_BG,
            "tooltip": {"trigger": "axis"},
            "legend": {"data": ["No Churn", "Churn"], "bottom": 0, "textStyle": {"fontSize": 11, "color": "#374151"}},
            "xAxis": {"type": "category", "data": [f"{x:.2f}" for x in ctr],
                      "axisLabel": {"interval": 7, "fontSize": 10, "color": "#8492a6"},
                      "axisLine": {"lineStyle": {"color": "#e8ecf0"}}},
            "yAxis": {"type": "value", "axisLabel": {"color": "#8492a6", "fontSize": 10},
                      "splitLine": {"lineStyle": {"color": "#f5f5f5"}}},
            "series": [
                {"name": "No Churn", "type": "bar", "data": hnc.tolist(), "itemStyle": {"color": "#1a2744", "opacity": 0.75}, "barGap": "-100%"},
                {"name": "Churn",    "type": "bar", "data": hc.tolist(),  "itemStyle": {"color": "#FF8C00", "opacity": 0.75}}
            ],
            "grid": {"left": "8%", "right": "4%", "bottom": "16%", "top": "4%"}
        }, height="280px")
        st.markdown('</div>', unsafe_allow_html=True)

    with col_r:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown('<p class="section-title">ROC Curve</p>', unsafe_allow_html=True)
        st.markdown('<p class="section-desc">True positive rate vs false positive rate at every threshold</p>', unsafe_allow_html=True)
        fpr, tpr, _ = roc_curve(oof['Churn_real'], oof['Churn_pred'])
        auc_val     = roc_auc_score(oof['Churn_real'], oof['Churn_pred'])
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=fpr.tolist(), y=tpr.tolist(), mode='lines', name=f'AUC={auc_val:.3f}', line=dict(color='#1a2744', width=2.5)))
        fig.add_trace(go.Scatter(x=[0,1], y=[0,1], mode='lines', name='Random', line=dict(color='#cbd5e0', dash='dash', width=1.5)))
        fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            font=dict(family='Inter', size=11, color='#374151'),
            margin=dict(t=8, b=36, l=44, r=8),
            xaxis=dict(title='False Positive Rate', gridcolor='#f5f5f5', linecolor='#e8ecf0'),
            yaxis=dict(title='True Positive Rate', gridcolor='#f5f5f5', linecolor='#e8ecf0'),
            legend=dict(x=0.62, y=0.08, bgcolor='rgba(0,0,0,0)'), height=280)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<p class="section-title">Confusion Matrix</p>', unsafe_allow_html=True)
    st.markdown('<p class="section-desc">Adjust the classification threshold to balance precision and recall</p>', unsafe_allow_html=True)
    threshold = st.slider("Threshold", 0.1, 0.9, 0.5, 0.05)
    yp = (oof['Churn_pred'] >= threshold).astype(int)
    cm = confusion_matrix(oof['Churn_real'], yp)
    tn, fp, fn, tp = cm.ravel()
    prec = tp/(tp+fp) if (tp+fp) > 0 else 0
    rec  = tp/(tp+fn) if (tp+fn) > 0 else 0
    f1   = 2*prec*rec/(prec+rec) if (prec+rec) > 0 else 0

    cc, cm_col = st.columns([1,1])
    with cc:
        fcm = go.Figure(go.Heatmap(
            z=cm, x=['Pred No Churn', 'Pred Churn'], y=['Act No Churn', 'Act Churn'],
            colorscale=[[0,'#f8fafc'],[1,'#1a2744']], text=cm,
            texttemplate='<b>%{text}</b>', showscale=False, textfont={"size":18}))
        fcm.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            font=dict(family='Inter', size=11), margin=dict(t=8,b=8,l=8,r=8), height=260)
        st.plotly_chart(fcm, use_container_width=True)
    with cm_col:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(kpi("Precision", f"{prec:.3f}", "Of predicted churners, how many actually churned", "#2ecc71", "#2ecc71"), unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(kpi("Recall", f"{rec:.3f}", "Of actual churners, how many did we catch", "#e74c3c", "#e74c3c"), unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(kpi("F1 Score", f"{f1:.3f}", "Balance between precision and recall", "#FF8C00", "#FF8C00"), unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# =============================================================================
# PAGE 4 — BUSINESS INSIGHTS
# =============================================================================
elif page == "Business Insights":
    st.markdown("""<div class="page-header">
        <p class="page-title">Business Insights</p>
        <p class="page-subtitle">What patterns drive churn? Where should the business focus retention efforts?</p>
    </div>""", unsafe_allow_html=True)

    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<p class="section-title">Contract Type — The Strongest Driver</p>', unsafe_allow_html=True)
    st.markdown('<p class="section-desc">Customers without long-term commitment churn at dramatically higher rates</p>', unsafe_allow_html=True)
    cd = dashboard.groupby('Contract')['churn_probability'].mean().sort_values(ascending=False)
    st_echarts({
        "backgroundColor": ECHART_BG,
        "tooltip": {"trigger": "axis", "formatter": "{b}: {c}"},
        "xAxis": {"type": "value", "axisLabel": {"color": "#8492a6", "fontSize": 10},
                  "splitLine": {"lineStyle": {"color": "#f5f5f5"}}},
        "yAxis": {"type": "category", "data": cd.index.tolist(),
                  "axisLabel": {"color": "#374151", "fontSize": 11},
                  "axisLine": {"lineStyle": {"color": "#e8ecf0"}}},
        "series": [{"type": "bar", "data": [round(v,4) for v in cd.values],
                    "itemStyle": {"color": "#1a2744", "borderRadius": [0,6,6,0]},
                    "label": {"show": True, "position": "right", "color": "#374151", "fontSize": 11}}],
        "grid": {"left": "20%", "right": "16%", "top": "5%", "bottom": "8%"}
    }, height="160px")
    st.markdown(f'<div class="insight">{get_contract_insight(dashboard)}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

    cl, cr = st.columns(2)

    with cl:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown('<p class="section-title">Internet Service</p>', unsafe_allow_html=True)
        st.markdown('<p class="section-desc">Fiber optic customers show highest churn risk despite paying more</p>', unsafe_allow_html=True)
        id_ = dashboard.groupby('InternetService')['churn_probability'].mean().sort_values(ascending=False)
        bc  = ["#e74c3c", "#f39c12", "#2ecc71"]
        st_echarts({
            "backgroundColor": ECHART_BG,
            "tooltip": {"trigger": "axis"},
            "xAxis": {"type": "category", "data": id_.index.tolist(),
                      "axisLabel": {"color": "#374151", "fontSize": 11},
                      "axisLine": {"lineStyle": {"color": "#e8ecf0"}}},
            "yAxis": {"type": "value", "axisLabel": {"color": "#8492a6", "fontSize": 10},
                      "splitLine": {"lineStyle": {"color": "#f5f5f5"}}},
            "series": [{"type": "bar",
                        "data": [{"value": round(v,4), "itemStyle": {"color": bc[i], "borderRadius": [4,4,0,0]}}
                                 for i,v in enumerate(id_.values)],
                        "label": {"show": True, "position": "top", "color": "#374151", "fontSize": 11}}],
            "grid": {"left": "8%", "right": "4%", "top": "16%", "bottom": "10%"}
        }, height="240px")
        st.markdown(f'<div class="insight">{get_internet_insight(dashboard)}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with cr:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown('<p class="section-title">Payment Method</p>', unsafe_allow_html=True)
        st.markdown('<p class="section-desc">Electronic check users are significantly more likely to churn</p>', unsafe_allow_html=True)
        pd_ = dashboard.groupby('PaymentMethod')['churn_probability'].mean().sort_values(ascending=False)
        sl  = [p.replace(' (automatic)', '\n(auto)') for p in pd_.index]
        st_echarts({
            "backgroundColor": ECHART_BG,
            "tooltip": {"trigger": "axis"},
            "xAxis": {"type": "category", "data": sl,
                      "axisLabel": {"color": "#374151", "fontSize": 10},
                      "axisLine": {"lineStyle": {"color": "#e8ecf0"}}},
            "yAxis": {"type": "value", "axisLabel": {"color": "#8492a6", "fontSize": 10},
                      "splitLine": {"lineStyle": {"color": "#f5f5f5"}}},
            "series": [{"type": "bar", "data": [round(v,4) for v in pd_.values],
                        "itemStyle": {"color": "#FF8C00", "borderRadius": [4,4,0,0]},
                        "label": {"show": True, "position": "top", "color": "#374151", "fontSize": 11}}],
            "grid": {"left": "8%", "right": "4%", "top": "16%", "bottom": "14%"}
        }, height="240px")
        st.markdown(f'<div class="insight">{get_payment_insight(dashboard)}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<p class="section-title">Tenure — The First 12 Months Are Critical</p>', unsafe_allow_html=True)
    st.markdown('<p class="section-desc">When do customers churn? Early tenure customers are the most vulnerable</p>', unsafe_allow_html=True)
    dsh = dashboard.copy()
    dsh['tg'] = pd.cut(dsh['Tenure'], bins=[0,6,12,24,36,72], labels=['0-6m','7-12m','13-24m','25-36m','37-72m'])
    td = dsh.groupby('tg', observed=True)['churn_probability'].mean()
    st_echarts({
        "backgroundColor": ECHART_BG,
        "tooltip": {"trigger": "axis"},
        "xAxis": {"type": "category", "data": td.index.tolist(),
                  "axisLabel": {"color": "#374151", "fontSize": 11},
                  "axisLine": {"lineStyle": {"color": "#e8ecf0"}},
                  "name": "Tenure Group", "nameLocation": "middle", "nameGap": 28,
                  "nameTextStyle": {"color": "#8492a6", "fontSize": 11}},
        "yAxis": {"type": "value", "axisLabel": {"color": "#8492a6", "fontSize": 10},
                  "splitLine": {"lineStyle": {"color": "#f5f5f5"}},
                  "name": "Avg Churn Probability", "nameLocation": "middle", "nameGap": 44,
                  "nameTextStyle": {"color": "#8492a6", "fontSize": 11}},
        "series": [{"type": "line", "data": [round(v,4) for v in td.values],
                    "smooth": True, "lineStyle": {"color": "#1a2744", "width": 3},
                    "areaStyle": {"color": "rgba(26,39,68,0.07)"},
                    "itemStyle": {"color": "#1a2744"},
                    "markPoint": {"data": [{"type": "max", "name": "Peak"}],
                                  "itemStyle": {"color": "#e74c3c"}}}],
        "grid": {"left": "10%", "right": "4%", "top": "10%", "bottom": "16%"}
    }, height="260px")
    st.markdown(f'<div class="insight">{get_tenure_insight(dashboard)}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
