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
from utils.design_system import COLORS, TYPOGRAPHY, SPACING, SHAPE, Tokens
from utils.insights import (
    get_overview_insights, get_contract_insight, get_internet_insight,
    get_payment_insight, get_tenure_insight, get_customer_risk_insight,
    get_model_insight
)

# ── Chart palette (all derived from design system) ───────────────────────────
C_AXIS    = Tokens.CHART_AXIS_COLOR     # SLATE_400  #7aa8c4
C_GRID    = Tokens.CHART_GRID           # SLATE_100  #e4f0f8
C_BORDER  = Tokens.CARD_BORDER          # SLATE_200  #d4e8f5
C_BODY    = Tokens.SECTION_TITLE_COLOR  # SLATE_900  #03314a
C_PRIMARY = Tokens.CHART_PRIMARY        # Baltic Blue #05668D
C_ACCENT  = Tokens.CHART_ACCENT         # Lime Moss   #A5BE00
C_AMBER   = COLORS.WARNING              # #c47d0e
C_YELLOW  = COLORS.ACCENT               # Lime Moss   #A5BE00  (highlight accent)
C_RED     = COLORS.DANGER               # #c0392b
C_GREEN   = COLORS.SUCCESS              # #679436  Sage Green
FONT      = TYPOGRAPHY.FONT             # "DM Sans"
FONT_MONO = TYPOGRAPHY.FONT_MONO        # "DM Mono"
ECHART_BG = "transparent"

st.set_page_config(
    page_title="ChurnGuard Analytics",
    page_icon="📡",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600;700&family=DM+Mono:wght@400;500&display=swap');

*, html, body {{ font-family: '{FONT}', sans-serif !important; box-sizing: border-box; }}

[data-testid="stAppViewContainer"],
[data-testid="stMain"],
.main {{ background-color: {Tokens.PAGE_BG} !important; }}
.block-container {{ padding: 2rem 2.5rem !important; max-width: 1400px !important; }}

/* ── Force sidebar always expanded ── */
section[data-testid="stSidebar"] {{
    transform: translateX(0) !important; display: block !important;
    min-width: 260px !important; width: 260px !important; visibility: visible !important;
}}
[data-testid="stSidebar"][aria-expanded="false"] {{
    transform: translateX(0) !important; min-width: 260px !important; width: 260px !important;
}}
[data-testid="stSidebarCollapseButton"] {{ display: none !important; }}
[data-testid="stSidebarCollapsedControl"] {{ display: none !important; }}
button[data-testid="collapsedControl"] {{ display: none !important; }}

/* ── Sidebar ── */
[data-testid="stSidebar"] {{
    background-color: {Tokens.SIDEBAR_BG} !important;
    padding: 1.5rem 1rem !important;
    border-right: 1px solid {Tokens.SIDEBAR_BORDER} !important;
}}
[data-testid="stSidebar"] section {{ padding: 0 !important; }}
[data-testid="stSidebar"] * {{ color: {COLORS.WHITE} !important; }}
[data-testid="stSidebar"] hr {{ border-color: {Tokens.SIDEBAR_BORDER} !important; margin: 1rem 0 !important; }}

/* ── Sidebar nav ── */
[data-testid="stSidebar"] .stRadio > label {{ display: none !important; }}
[data-testid="stSidebar"] .stRadio > div {{ gap: 1px !important; }}
[data-testid="stSidebar"] .stRadio label {{
    background: transparent !important; border-radius: {SHAPE.RADIUS_SM} !important;
    padding: 9px 12px !important; font-size: 0.86rem !important;
    font-weight: {TYPOGRAPHY.NORMAL} !important; line-height: {TYPOGRAPHY.TIGHT} !important;
    cursor: pointer !important; transition: background 0.12s ease, color 0.12s ease !important;
    border: none !important; outline: none !important; box-shadow: none !important;
    color: rgba(255,255,255,0.5) !important; width: 100% !important; display: block !important;
}}
[data-testid="stSidebar"] .stRadio label:hover {{
    background: rgba(255,255,255,0.08) !important; color: rgba(255,255,255,0.9) !important;
}}
[data-testid="stSidebar"] .stRadio label p {{ margin: 0 !important; font-size: 0.86rem !important; }}
[data-testid="stSidebar"] .stRadio label > div:first-child {{ display: none !important; }}
[data-testid="stSidebar"] .stMultiSelect label,
[data-testid="stSidebar"] .stSlider label {{
    font-size: {TYPOGRAPHY.XS} !important; text-transform: uppercase !important;
    letter-spacing: 0.8px !important; color: rgba(255,255,255,0.4) !important;
    margin-bottom: {SPACING.S1} !important;
}}
[data-testid="stSidebar"] .stMultiSelect [data-baseweb="select"] > div {{
    background: rgba(255,255,255,0.07) !important;
    border: 1px solid rgba(255,255,255,0.12) !important;
    border-radius: {SHAPE.RADIUS_SM} !important;
}}

/* ── Remove column borders ── */
[data-testid="stHorizontalBlock"] > div,
[data-testid="column"] {{
    border: none !important; outline: none !important;
    box-shadow: none !important; background: transparent !important;
}}

/* ── Page header ── */
.page-header {{
    margin-bottom: 1.5rem; padding-bottom: 1rem;
    border-bottom: 1px solid {Tokens.CARD_BORDER};
    display: flex; align-items: flex-start; justify-content: space-between;
}}
.page-title {{
    font-size: {Tokens.PAGE_TITLE_SIZE}; font-weight: {Tokens.PAGE_TITLE_WEIGHT};
    color: {Tokens.PAGE_TITLE_COLOR}; margin: 0 0 3px 0;
    line-height: {TYPOGRAPHY.TIGHT}; letter-spacing: -0.3px;
}}
.page-subtitle {{ font-size: {Tokens.PAGE_SUB_SIZE}; color: {Tokens.PAGE_SUB_COLOR}; margin: 0; }}
.page-badge {{
    background: {Tokens.BADGE_BG}; color: {Tokens.BADGE_COLOR};
    font-size: {TYPOGRAPHY.XS}; font-weight: {TYPOGRAPHY.SEMI};
    padding: 4px 10px; border-radius: {SHAPE.RADIUS_FULL};
    letter-spacing: 0.5px; text-transform: uppercase; white-space: nowrap; margin-top: {SPACING.S1};
}}

/* ── KPI Cards ── */
.kpi-card {{
    background: {Tokens.CARD_BG}; border: 1px solid {Tokens.CARD_BORDER};
    border-radius: {Tokens.CARD_RADIUS}; padding: 18px 20px 16px 20px;
    position: relative; overflow: hidden;
    box-shadow: {Tokens.CARD_SHADOW}; transition: box-shadow 0.2s;
}}
.kpi-card:hover {{ box-shadow: {Tokens.CARD_HOVER_SHADOW}; }}
.kpi-accent {{ position: absolute; top: 0; left: 0; width: 100%; height: 3px; border-radius: {Tokens.CARD_RADIUS} {Tokens.CARD_RADIUS} 0 0; }}
.kpi-label {{
    font-size: {Tokens.KPI_LABEL_SIZE}; font-weight: {Tokens.KPI_LABEL_WEIGHT};
    color: {Tokens.KPI_LABEL_COLOR}; text-transform: uppercase;
    letter-spacing: 0.9px; margin: {SPACING.S2} 0 {SPACING.S1} 0;
}}
.kpi-value {{
    font-size: 1.9rem; font-weight: {TYPOGRAPHY.BOLD};
    color: {Tokens.PAGE_TITLE_COLOR}; margin: 0 0 {SPACING.S1} 0;
    line-height: 1; letter-spacing: -0.5px;
}}
.kpi-delta {{ font-size: {Tokens.KPI_DELTA_SIZE}; color: {Tokens.KPI_DELTA_COLOR}; margin: 0; font-weight: {TYPOGRAPHY.NORMAL}; }}

/* ── Section cards ── */
.section-card {{
    background: {Tokens.CARD_BG}; border: 1px solid {Tokens.CARD_BORDER};
    border-radius: {Tokens.CARD_RADIUS}; padding: 20px 22px 18px 22px;
    margin-bottom: {SPACING.S4}; box-shadow: {Tokens.CARD_SHADOW};
}}
.section-header {{ display: flex; align-items: flex-start; justify-content: space-between; margin-bottom: 14px; }}
.section-title {{
    font-size: {Tokens.SECTION_TITLE_SIZE}; font-weight: {Tokens.SECTION_TITLE_WEIGHT};
    color: {Tokens.SECTION_TITLE_COLOR}; margin: 0 0 2px 0; letter-spacing: -0.1px;
}}
.section-desc {{ font-size: {Tokens.SECTION_DESC_SIZE}; color: {Tokens.SECTION_DESC_COLOR}; margin: 0; }}
.section-tag {{
    font-size: {TYPOGRAPHY.XS}; font-weight: {TYPOGRAPHY.SEMI};
    padding: 3px 8px; border-radius: {SHAPE.RADIUS_FULL}; white-space: nowrap;
}}

/* ── Insight box ── */
.insight {{
    background: {Tokens.INSIGHT_BG}; border-left: 3px solid {Tokens.INSIGHT_ACCENT};
    border-radius: 0 {SHAPE.RADIUS_SM} {SHAPE.RADIUS_SM} 0;
    padding: 10px 14px; margin-top: {SPACING.S3};
    font-size: 0.82rem; color: {COLORS.SLATE_700}; line-height: {TYPOGRAPHY.RELAXED};
}}

/* ── Feature importance ── */
.fi-row {{ display: flex; align-items: center; gap: 10px; padding: 6px 0; border-bottom: 1px solid {Tokens.BORDER_SUBTLE}; }}
.fi-label {{ font-size: 0.82rem; color: {COLORS.SLATE_700}; font-weight: {TYPOGRAPHY.MEDIUM}; min-width: 140px; }}
.fi-bar-bg {{ flex: 1; height: 8px; background: {COLORS.SLATE_100}; border-radius: {SPACING.S1}; overflow: hidden; }}
.fi-bar {{ height: 100%; border-radius: {SPACING.S1}; }}
.fi-pct {{ font-size: 0.78rem; color: {Tokens.KPI_LABEL_COLOR}; min-width: 38px; text-align: right; font-family: '{FONT_MONO}', monospace; }}

/* ── Stat pill ── */
.stat-pill {{
    display: inline-flex; align-items: center; gap: 6px;
    background: {Tokens.PAGE_BG}; border: 1px solid {Tokens.CARD_BORDER};
    border-radius: {SHAPE.RADIUS_SM}; padding: 6px 12px; font-size: 0.8rem; color: {COLORS.SLATE_700};
}}
.stat-pill b {{ color: {Tokens.PAGE_TITLE_COLOR}; }}

/* ── Divider ── */
.divider {{ height: 1px; background: {Tokens.DIVIDER}; margin: {SPACING.S5} 0; }}

/* ── Table ── */
div[data-testid="stDataFrame"] {{
    border: 1px solid {Tokens.CARD_BORDER} !important;
    border-radius: {SHAPE.RADIUS_MD} !important;
    overflow: hidden !important;
}}
div[data-testid="stDataFrame"] > div {{ background: {Tokens.CARD_BG} !important; }}

/* ── Download button ── */
.stDownloadButton button {{
    background: {Tokens.PAGE_TITLE_COLOR} !important; color: {COLORS.WHITE} !important;
    border: none !important; border-radius: {SHAPE.RADIUS_SM} !important;
    font-size: 0.82rem !important; padding: 7px 18px !important; font-weight: {TYPOGRAPHY.MEDIUM} !important;
}}

/* ── Hide branding ── */
#MainMenu, footer, header {{ visibility: hidden; }}

</style>
""", unsafe_allow_html=True)

# ── Data ──────────────────────────────────────────────────────────────────────
@st.cache_data
def get_data():
    return load_all()

dashboard, oof = get_data()
kpis = get_kpis(dashboard, oof)

# ── Feature importance ────────────────────────────────────────────────────────
@st.cache_data
def compute_feature_importance(df):
    features = {
        'Contract'       : 'Contract Type',
        'Tenure'         : 'Tenure (months)',
        'MonthlyCharges' : 'Monthly Charges',
        'TotalCharges'   : 'Total Charges',
        'InternetService': 'Internet Service',
        'PaymentMethod'  : 'Payment Method',
        'SeniorCitizen'  : 'Senior Citizen',
        'Partner'        : 'Partner',
        'Dependents'     : 'Dependents',
    }
    scores = {}
    for col, label in features.items():
        if col not in df.columns:
            continue
        if df[col].dtype in [np.float64, np.int64, float, int]:
            corr = abs(df[col].corr(df['churn_probability']))
        else:
            dummies = pd.get_dummies(df[col], drop_first=True)
            corr = dummies.corrwith(df['churn_probability']).abs().max()
        scores[label] = round(float(corr), 4)
    total = sum(scores.values())
    return {k: v/total for k, v in sorted(scores.items(), key=lambda x: -x[1])}

feature_importance = compute_feature_importance(dashboard)

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(f"""
    <div style='margin-bottom:1.5rem'>
        <div style='font-size:{TYPOGRAPHY.XS};font-weight:{TYPOGRAPHY.SEMI};text-transform:uppercase;
                    letter-spacing:1.2px;color:rgba(255,255,255,0.35);margin-bottom:6px'>Platform</div>
        <div style='font-size:1.15rem;font-weight:{TYPOGRAPHY.BOLD};color:{COLORS.WHITE};
                    letter-spacing:-0.3px'>ChurnGuard</div>
        <div style='font-size:0.8rem;color:rgba(255,255,255,0.45);margin-top:2px'>Telco Analytics</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"<div style='font-size:{TYPOGRAPHY.XS};font-weight:{TYPOGRAPHY.SEMI};text-transform:uppercase;"
                f"letter-spacing:1px;color:rgba(255,255,255,0.3);margin-bottom:6px'>Navigation</div>",
                unsafe_allow_html=True)

    page = st.radio("", ["Overview", "Customer Risk", "Model Performance", "Business Insights", "Segments"])

    st.markdown("---")
    st.markdown(f"<div style='font-size:{TYPOGRAPHY.XS};font-weight:{TYPOGRAPHY.SEMI};text-transform:uppercase;"
                f"letter-spacing:1px;color:rgba(255,255,255,0.3);margin-bottom:10px'>Model Summary</div>",
                unsafe_allow_html=True)
    st.markdown(f"""
    <div style='display:flex;flex-direction:column;gap:9px'>
        <div style='display:flex;justify-content:space-between;font-size:0.82rem'>
            <span style='color:rgba(255,255,255,0.45)'>Algorithm</span>
            <span style='color:{COLORS.WHITE};font-weight:{TYPOGRAPHY.SEMI};font-family:"{FONT_MONO}",monospace;font-size:0.78rem'>XGBoost</span>
        </div>
        <div style='display:flex;justify-content:space-between;font-size:0.82rem'>
            <span style='color:rgba(255,255,255,0.45)'>Validation</span>
            <span style='color:{COLORS.WHITE};font-weight:{TYPOGRAPHY.SEMI};font-family:"{FONT_MONO}",monospace;font-size:0.78rem'>10-Fold CV</span>
        </div>
        <div style='display:flex;justify-content:space-between;font-size:0.82rem'>
            <span style='color:rgba(255,255,255,0.45)'>OOF AUC</span>
            <span style='color:{C_YELLOW};font-weight:{TYPOGRAPHY.BOLD};font-family:"{FONT_MONO}",monospace'>{kpis['oof_auc']:.3f}</span>
        </div>
        <div style='display:flex;justify-content:space-between;font-size:0.82rem'>
            <span style='color:rgba(255,255,255,0.45)'>Test Set</span>
            <span style='color:{COLORS.WHITE};font-weight:{TYPOGRAPHY.SEMI};font-family:"{FONT_MONO}",monospace;font-size:0.78rem'>{kpis['total']:,}</span>
        </div>
        <div style='display:flex;justify-content:space-between;font-size:0.82rem'>
            <span style='color:rgba(255,255,255,0.45)'>Avg Risk</span>
            <span style='color:{COLORS.WHITE};font-weight:{TYPOGRAPHY.SEMI};font-family:"{FONT_MONO}",monospace;font-size:0.78rem'>{kpis["avg_prob"]:.1%}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("---")
    st.markdown(f"<div style='font-size:0.7rem;color:rgba(255,255,255,0.2);line-height:{TYPOGRAPHY.RELAXED}'>"
                f"ChurnGuard v1.0<br>Daniel Padilla · 2026</div>", unsafe_allow_html=True)

# ── Helpers ───────────────────────────────────────────────────────────────────
def safe_val(v, default=0):
    try:
        return default if pd.isna(v) else float(v)
    except Exception:
        return default

# Echarts style helpers — all colors from tokens
def ax_label(size=10):   return {"color": C_AXIS,  "fontSize": size}
def ax_label_b(size=11): return {"color": C_BODY,  "fontSize": size}
def ax_line():  return {"lineStyle": {"color": C_BORDER}}
def sp_line():  return {"lineStyle": {"color": C_GRID}}
def name_style(): return {"color": C_AXIS, "fontSize": 11}

def kpi_card(label, value, delta="", color=None, accent=None):
    color  = color  or Tokens.PAGE_TITLE_COLOR
    accent = accent or Tokens.PAGE_TITLE_COLOR
    return (f'<div class="kpi-card">'
            f'<div class="kpi-accent" style="background:{accent}"></div>'
            f'<p class="kpi-label">{label}</p>'
            f'<p class="kpi-value" style="color:{color}">{value}</p>'
            f'<p class="kpi-delta">{delta}</p></div>')

def feature_importance_html(fi_dict, top_n=9):
    items  = list(fi_dict.items())[:top_n]
    max_v  = items[0][1] if items else 1
    palette = [COLORS.PRIMARY_700, COLORS.PRIMARY_600, COLORS.PRIMARY_600, COLORS.PRIMARY_500, "#7aa8c4", "#b8d4e8",
               "#c4c9fb", "#d9dbfd", "#eceefe", "#f0f1ff", "#f5f6ff"]
    rows = ""
    for i, (label, pct) in enumerate(items):
        bar_w = int((pct / max_v) * 100)
        rows += (f'<div class="fi-row">'
                 f'<div class="fi-label">{label}</div>'
                 f'<div class="fi-bar-bg"><div class="fi-bar" style="width:{bar_w}%;background:{palette[min(i,8)]}"></div></div>'
                 f'<div class="fi-pct">{pct:.1%}</div></div>')
    return f'<div style="margin-top:{SPACING.S1}">{rows}</div>'

# =============================================================================
# PAGE 1 — OVERVIEW
# =============================================================================
if page == "Overview":
    st.markdown("""<div class="page-header"><div>
        <p class="page-title">Churn Intelligence Overview</p>
        <p class="page-subtitle">How many customers are at risk — and how urgent is it?</p>
        </div><span class="page-badge">Live · Test Set</span></div>""", unsafe_allow_html=True)

    c1, c2, c3, c4, c5 = st.columns(5)
    with c1: st.markdown(kpi_card("Total Customers",  f"{kpis['total']:,}",             "Test set",                           accent=COLORS.PRIMARY_700), unsafe_allow_html=True)
    with c2: st.markdown(kpi_card("At Risk",           f"{kpis['at_risk']:,}",           f"{kpis['at_risk_pct']:.1f}% · prob ≥25%", C_AMBER,  C_YELLOW),        unsafe_allow_html=True)
    with c3: st.markdown(kpi_card("High Risk",         f"{kpis['high_risk']:,}",         f"{kpis['high_risk_pct']:.1f}% · prob ≥50%", C_RED,   COLORS.DANGER),   unsafe_allow_html=True)
    with c4: st.markdown(kpi_card("Critical",          f"{kpis['critical']:,}",          "prob ≥75%",                          COLORS.CRITICAL, COLORS.CRITICAL), unsafe_allow_html=True)
    with c5: st.markdown(kpi_card("Model AUC",         f"{kpis['oof_auc']:.3f}",         "Out-of-Fold · No leakage",           C_AMBER,  C_YELLOW),              unsafe_allow_html=True)

    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
    col_l, col_r = st.columns(2)

    with col_l:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-header"><div>'
                    '<p class="section-title">Churn Risk Distribution</p>'
                    '<p class="section-desc">Predicted churn probability across all customers</p>'
                    '</div></div>', unsafe_allow_html=True)
        hist_data, bin_edges = np.histogram(dashboard['churn_probability'], bins=40)
        bin_centers = [(bin_edges[i]+bin_edges[i+1])/2 for i in range(len(bin_edges)-1)]
        st_echarts({
            "backgroundColor": ECHART_BG,
            "tooltip": {"trigger": "axis", "axisPointer": {"type": "shadow"}},
            "xAxis": {"type": "category", "data": [f"{x:.2f}" for x in bin_centers],
                      "axisLabel": {**ax_label(), "interval": 7}, "axisLine": ax_line(),
                      "name": "Churn Probability", "nameLocation": "middle", "nameGap": 28,
                      "nameTextStyle": name_style()},
            "yAxis": {"type": "value", "axisLabel": ax_label(), "splitLine": sp_line(),
                      "name": "Customers", "nameLocation": "middle", "nameGap": 40,
                      "nameTextStyle": name_style()},
            "series": [{"type": "bar", "data": hist_data.tolist(),
                        "itemStyle": {"color": C_PRIMARY, "borderRadius": [3,3,0,0]}}],
            "grid": {"left": "12%", "right": "4%", "bottom": "16%", "top": "4%"}
        }, height="260px")
        st.markdown(f'<div class="insight">{get_overview_insights(dashboard, kpis)}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col_r:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-header"><div>'
                    '<p class="section-title">Customers by Risk Level</p>'
                    '<p class="section-desc">Segmentation across four risk tiers</p>'
                    '</div></div>', unsafe_allow_html=True)
        risk_counts = dashboard['risk_level'].value_counts().reindex(['Low','Medium','High','Critical']).fillna(0)
        st_echarts({
            "backgroundColor": ECHART_BG,
            "tooltip": {"trigger": "item", "formatter": "{b}: {c} customers ({d}%)"},
            "legend": {"orient": "horizontal", "bottom": "0%", "textStyle": {"fontSize": 11, "color": C_BODY}},
            "series": [{"type": "pie", "radius": ["42%","68%"], "center": ["50%","44%"],
                "data": [{"value": int(v), "name": k, "itemStyle": {"color": RISK_COLORS[k]}}
                         for k, v in zip(risk_counts.index, risk_counts.values)],
                "label": {"show": True, "formatter": "{b}: {c}", "fontSize": 11, "color": C_BODY},
                "emphasis": {"itemStyle": {"shadowBlur": 8, "shadowColor": "rgba(0,0,0,0.15)"}}}]
        }, height="260px")
        high_critical = int(risk_counts.get('High',0)) + int(risk_counts.get('Critical',0))
        st.markdown(f'<div class="insight"><b>{high_critical} customers</b> require proactive retention (High + Critical) — '
                    f'<b>{high_critical/kpis["total"]:.1%}</b> of the base. Prioritize these for immediate outreach.</div>',
                    unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown(f'<div class="section-header"><div>'
                f'<p class="section-title">Highest Risk Customers</p>'
                f'<p class="section-desc">Customers with the highest predicted churn probability — prioritize for retention</p>'
                f'</div><span class="section-tag" style="background:{COLORS.DANGER_LT};color:#991b1b">⚠ Immediate Action</span></div>',
                unsafe_allow_html=True)
    top10 = dashboard.nlargest(10, 'churn_probability')[
        ['id','churn_probability','risk_level','Contract','Tenure','MonthlyCharges','TotalCharges','InternetService','PaymentMethod']
    ].copy()
    top10['Churn Prob'] = top10['churn_probability'].apply(lambda x: f'{x:.1%}')
    top10['Monthly $']  = top10['MonthlyCharges'].apply(lambda x: f'${x:.2f}')
    top10['Total $']    = top10['TotalCharges'].apply(lambda x: f'${x:.2f}')
    top10['Tenure']     = top10['Tenure'].apply(lambda x: f'{int(x)} mo')
    display = top10[['id','Churn Prob','risk_level','Contract','Tenure','Monthly $','Total $','InternetService','PaymentMethod']].rename(columns={'risk_level':'Risk','id':'Customer ID'})
    st.dataframe(display, use_container_width=True, hide_index=True)
    st.markdown('</div>', unsafe_allow_html=True)

# =============================================================================
# PAGE 2 — CUSTOMER RISK
# =============================================================================
elif page == "Customer Risk":
    st.markdown("""<div class="page-header"><div>
        <p class="page-title">Customer Risk Explorer</p>
        <p class="page-subtitle">Filter and drill into individual customer churn risk profiles</p>
        </div><span class="page-badge">Interactive</span></div>""", unsafe_allow_html=True)

    with st.sidebar:
        st.markdown("---")
        st.markdown(f"<div style='font-size:{TYPOGRAPHY.XS};font-weight:{TYPOGRAPHY.SEMI};text-transform:uppercase;"
                    f"letter-spacing:1px;color:rgba(255,255,255,0.3);margin-bottom:{SPACING.S2}'>Filters</div>",
                    unsafe_allow_html=True)
        risk_filter     = st.multiselect("Risk Level", ['Low','Medium','High','Critical'], default=['Medium','High','Critical'])
        contract_filter = st.multiselect("Contract", sorted(dashboard['Contract'].unique()), default=sorted(dashboard['Contract'].unique()))
        internet_filter = st.multiselect("Internet Service", sorted(dashboard['InternetService'].unique()), default=sorted(dashboard['InternetService'].unique()))
        prob_threshold  = st.slider("Min Probability", 0.0, 1.0, 0.25, 0.05)

    filtered = dashboard[
        (dashboard['risk_level'].isin(risk_filter)) &
        (dashboard['Contract'].isin(contract_filter)) &
        (dashboard['InternetService'].isin(internet_filter)) &
        (dashboard['churn_probability'] >= prob_threshold)
    ].copy()

    avg_prob   = filtered['churn_probability'].mean() if len(filtered) > 0 else 0
    avg_mc     = filtered['MonthlyCharges'].mean()    if len(filtered) > 0 else 0
    avg_tenure = filtered['Tenure'].mean()            if len(filtered) > 0 else 0

    c1, c2, c3, c4 = st.columns(4)
    with c1: st.markdown(kpi_card("Filtered Customers",    f"{len(filtered):,}",  f"{len(filtered)/kpis['total']:.1%} of total", accent=COLORS.PRIMARY_700), unsafe_allow_html=True)
    with c2: st.markdown(kpi_card("Avg Churn Probability", f"{avg_prob:.1%}",      "Selected segment", C_RED,   COLORS.DANGER),  unsafe_allow_html=True)
    with c3: st.markdown(kpi_card("Avg Monthly Charges",   f"${avg_mc:.2f}",       "Selected segment", C_AMBER, C_YELLOW),       unsafe_allow_html=True)
    with c4: st.markdown(kpi_card("Avg Tenure",            f"{avg_tenure:.0f} mo", "Selected segment", accent=COLORS.CRITICAL),  unsafe_allow_html=True)

    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown(f'<div class="insight">{get_customer_risk_insight(filtered, dashboard)}</div>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    display_cols = ['id','churn_probability','risk_level','Contract','Tenure','MonthlyCharges','TotalCharges',
                    'InternetService','PaymentMethod','Gender','SeniorCitizen','Partner','Dependents']
    display_cols = [c for c in display_cols if c in filtered.columns]
    fd = filtered[display_cols].copy().sort_values('churn_probability', ascending=False)
    fd['churn_probability'] = fd['churn_probability'].apply(lambda x: f'{x:.1%}')
    fd['MonthlyCharges']    = fd['MonthlyCharges'].apply(lambda x: f'${x:.2f}')
    fd['Tenure']            = fd['Tenure'].apply(lambda x: f'{int(x)} mo')
    st.dataframe(fd, use_container_width=True, hide_index=True, height=480)
    col_dl, _ = st.columns([1,4])
    with col_dl:
        st.download_button("⬇ Export CSV", filtered[display_cols].to_csv(index=False), "churn_risk.csv", "text/csv")
    st.markdown('</div>', unsafe_allow_html=True)

# =============================================================================
# PAGE 3 — MODEL PERFORMANCE
# =============================================================================
elif page == "Model Performance":
    st.markdown(f"""<div class="page-header"><div>
        <p class="page-title">Model Performance</p>
        <p class="page-subtitle">XGBoost · 10-Fold Stratified CV · Honest OOF evaluation with no data leakage</p>
        </div><span class="page-badge">XGBoost · AUC {kpis['oof_auc']:.3f}</span></div>""", unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    with c1: st.markdown(kpi_card("OOF AUC",       f"{kpis['oof_auc']:.4f}", "No data leakage",    C_AMBER,             C_YELLOW),        unsafe_allow_html=True)
    with c2: st.markdown(kpi_card("Algorithm",      "XGBoost",                "Gradient Boosting",  accent=COLORS.PRIMARY_700),             unsafe_allow_html=True)
    with c3: st.markdown(kpi_card("CV Folds",       "10",                     "Stratified K-Fold",  accent=COLORS.CRITICAL),               unsafe_allow_html=True)
    with c4: st.markdown(kpi_card("Train Samples",  f"{len(oof):,}",          "OOF predictions",    accent=C_GREEN),                       unsafe_allow_html=True)

    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
    st.markdown(f'<div class="insight" style="margin-bottom:{SPACING.S4}">{get_model_insight(kpis["oof_auc"])}</div>', unsafe_allow_html=True)

    col_l, col_r = st.columns(2)

    with col_l:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-header"><div>'
                    '<p class="section-title">OOF Prediction Distribution</p>'
                    '<p class="section-desc">Separation between churners and non-churners</p>'
                    '</div></div>', unsafe_allow_html=True)
        cp  = oof[oof['Churn_real'] == 1]['Churn_pred'].values
        ncp = oof[oof['Churn_real'] == 0]['Churn_pred'].values
        hc,  ec  = np.histogram(cp,  bins=40, range=(0,1))
        hnc, enc = np.histogram(ncp, bins=40, range=(0,1))
        ctr = [(ec[i]+ec[i+1])/2 for i in range(len(ec)-1)]
        st_echarts({
            "backgroundColor": ECHART_BG,
            "tooltip": {"trigger": "axis"},
            "legend": {"data": ["No Churn","Churn"], "bottom": 0, "textStyle": {"fontSize": 11, "color": C_BODY}},
            "xAxis": {"type": "category", "data": [f"{x:.2f}" for x in ctr],
                      "axisLabel": {**ax_label(), "interval": 7}, "axisLine": ax_line()},
            "yAxis": {"type": "value", "axisLabel": ax_label(), "splitLine": sp_line()},
            "series": [
                {"name": "No Churn", "type": "bar", "data": hnc.tolist(),
                 "itemStyle": {"color": COLORS.PRIMARY_700, "opacity": 0.7}, "barGap": "-100%"},
                {"name": "Churn",    "type": "bar", "data": hc.tolist(),
                 "itemStyle": {"color": C_YELLOW, "opacity": 0.75}}
            ],
            "grid": {"left": "8%", "right": "4%", "bottom": "16%", "top": "4%"}
        }, height="260px")
        st.markdown('</div>', unsafe_allow_html=True)

    with col_r:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-header"><div>'
                    '<p class="section-title">ROC Curve</p>'
                    '<p class="section-desc">True positive rate vs false positive rate</p>'
                    '</div></div>', unsafe_allow_html=True)
        fpr, tpr, _ = roc_curve(oof['Churn_real'], oof['Churn_pred'])
        auc_val     = roc_auc_score(oof['Churn_real'], oof['Churn_pred'])
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=fpr.tolist(), y=tpr.tolist(), mode='lines',
            name=f'AUC = {auc_val:.3f}', line=dict(color=C_PRIMARY, width=2.5),
            fill='tozeroy', fillcolor='rgba(5,102,141,0.06)'))
        fig.add_trace(go.Scatter(x=[0,1], y=[0,1], mode='lines', name='Random',
            line=dict(color=COLORS.SLATE_300, dash='dash', width=1.5)))
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            font=dict(family=FONT, size=11, color=C_BODY),
            margin=dict(t=8, b=36, l=44, r=8),
            xaxis=dict(title='False Positive Rate', gridcolor=C_GRID, linecolor=C_BORDER, zeroline=False),
            yaxis=dict(title='True Positive Rate',  gridcolor=C_GRID, linecolor=C_BORDER, zeroline=False),
            legend=dict(x=0.58, y=0.08, bgcolor='rgba(0,0,0,0)'), height=260)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
    col_fi, col_cm = st.columns(2)

    with col_fi:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown(f'<div class="section-header"><div>'
                    f'<p class="section-title">Feature Importance</p>'
                    f'<p class="section-desc">Correlation-based driver ranking — relative contribution to churn probability</p>'
                    f'</div><span class="section-tag" style="background:{COLORS.PRIMARY_50};color:{COLORS.PRIMARY_700}">Data-driven</span></div>',
                    unsafe_allow_html=True)
        st.markdown(feature_importance_html(feature_importance, top_n=9), unsafe_allow_html=True)
        top_feat = list(feature_importance.keys())[0]
        st.markdown(f'<div class="insight"><b>{top_feat}</b> is the strongest driver, followed by '
                    f'<b>{list(feature_importance.keys())[1]}</b>. These features should anchor any retention strategy.</div>',
                    unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col_cm:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-header"><div>'
                    '<p class="section-title">Confusion Matrix</p>'
                    '<p class="section-desc">Adjust threshold to balance precision and recall</p>'
                    '</div></div>', unsafe_allow_html=True)
        threshold = st.slider("Classification Threshold", 0.1, 0.9, 0.5, 0.05)
        yp = (oof['Churn_pred'] >= threshold).astype(int)
        cm = confusion_matrix(oof['Churn_real'], yp)
        tn, fp, fn, tp = cm.ravel()
        prec = tp/(tp+fp) if (tp+fp) > 0 else 0
        rec  = tp/(tp+fn) if (tp+fn) > 0 else 0
        f1   = 2*prec*rec/(prec+rec) if (prec+rec) > 0 else 0
        fcm = go.Figure(go.Heatmap(
            z=cm, x=['Pred No Churn','Pred Churn'], y=['Act No Churn','Act Churn'],
            colorscale=[[0, COLORS.PRIMARY_50],[1, C_PRIMARY]],
            text=cm, texttemplate='<b>%{text}</b>', showscale=False,
            textfont={"size": 18, "color": COLORS.WHITE}))
        fcm.update_layout(
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            font=dict(family=FONT, size=11), margin=dict(t=8,b=8,l=8,r=8), height=200)
        st.plotly_chart(fcm, use_container_width=True)
        mc1, mc2, mc3 = st.columns(3)
        with mc1: st.markdown(kpi_card("Precision", f"{prec:.3f}", "Of predicted churners", C_GREEN,  C_GREEN),  unsafe_allow_html=True)
        with mc2: st.markdown(kpi_card("Recall",    f"{rec:.3f}",  "Churners captured",     C_RED,    C_RED),    unsafe_allow_html=True)
        with mc3: st.markdown(kpi_card("F1 Score",  f"{f1:.3f}",   "Harmonic mean",         C_AMBER,  C_YELLOW), unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

# =============================================================================
# PAGE 4 — BUSINESS INSIGHTS
# =============================================================================
elif page == "Business Insights":
    st.markdown("""<div class="page-header"><div>
        <p class="page-title">Business Insights</p>
        <p class="page-subtitle">What patterns drive churn? Where should retention efforts focus?</p>
        </div><span class="page-badge">Strategic</span></div>""", unsafe_allow_html=True)

    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown(f'<div class="section-header"><div>'
                f'<p class="section-title">Contract Type — The Strongest Driver</p>'
                f'<p class="section-desc">Customers without long-term commitment churn at dramatically higher rates</p>'
                f'</div><span class="section-tag" style="background:{COLORS.DANGER_LT};color:#991b1b">High Impact</span></div>',
                unsafe_allow_html=True)
    cd = dashboard.groupby('Contract')['churn_probability'].mean().sort_values(ascending=False)
    st_echarts({
        "backgroundColor": ECHART_BG,
        "tooltip": {"trigger": "axis", "formatter": "{b}: {c}"},
        "xAxis": {"type": "value", "axisLabel": ax_label(), "splitLine": sp_line()},
        "yAxis": {"type": "category", "data": cd.index.tolist(),
                  "axisLabel": ax_label_b(), "axisLine": ax_line()},
        "series": [{"type": "bar", "data": [round(safe_val(v), 4) for v in cd.values],
                    "itemStyle": {"color": C_PRIMARY, "borderRadius": [0,6,6,0]},
                    "label": {"show": True, "position": "right", "color": C_BODY, "fontSize": 11}}],
        "grid": {"left": "22%", "right": "16%", "top": "5%", "bottom": "8%"}
    }, height="160px")
    st.markdown(f'<div class="insight">{get_contract_insight(dashboard)}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
    cl, cr = st.columns(2)

    with cl:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-header"><div>'
                    '<p class="section-title">Internet Service</p>'
                    '<p class="section-desc">Fiber optic customers show highest churn despite paying more</p>'
                    '</div></div>', unsafe_allow_html=True)
        id_ = dashboard.groupby('InternetService')['churn_probability'].mean().sort_values(ascending=False)
        bc  = [C_RED, C_YELLOW, C_GREEN]
        st_echarts({
            "backgroundColor": ECHART_BG,
            "tooltip": {"trigger": "axis"},
            "xAxis": {"type": "category", "data": id_.index.tolist(), "axisLabel": ax_label_b(), "axisLine": ax_line()},
            "yAxis": {"type": "value", "axisLabel": ax_label(), "splitLine": sp_line()},
            "series": [{"type": "bar",
                        "data": [{"value": round(safe_val(v), 4), "itemStyle": {"color": bc[i], "borderRadius": [4,4,0,0]}}
                                 for i,v in enumerate(id_.values)],
                        "label": {"show": True, "position": "top", "color": C_BODY, "fontSize": 11}}],
            "grid": {"left": "8%", "right": "4%", "top": "16%", "bottom": "10%"}
        }, height="240px")
        st.markdown(f'<div class="insight">{get_internet_insight(dashboard)}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with cr:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-header"><div>'
                    '<p class="section-title">Payment Method</p>'
                    '<p class="section-desc">Electronic check users are significantly more likely to churn</p>'
                    '</div></div>', unsafe_allow_html=True)
        pd_ = dashboard.groupby('PaymentMethod')['churn_probability'].mean().sort_values(ascending=False)
        sl  = [p.replace(' (automatic)','\n(auto)') for p in pd_.index]
        st_echarts({
            "backgroundColor": ECHART_BG,
            "tooltip": {"trigger": "axis"},
            "xAxis": {"type": "category", "data": sl, "axisLabel": {**ax_label_b(), "fontSize": 10}, "axisLine": ax_line()},
            "yAxis": {"type": "value", "axisLabel": ax_label(), "splitLine": sp_line()},
            "series": [{"type": "bar", "data": [round(safe_val(v), 4) for v in pd_.values],
                        "itemStyle": {"color": C_YELLOW, "borderRadius": [4,4,0,0]},
                        "label": {"show": True, "position": "top", "color": C_BODY, "fontSize": 11}}],
            "grid": {"left": "8%", "right": "4%", "top": "16%", "bottom": "14%"}
        }, height="240px")
        st.markdown(f'<div class="insight">{get_payment_insight(dashboard)}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown(f'<div class="section-header"><div>'
                f'<p class="section-title">Tenure — The First 12 Months Are Critical</p>'
                f'<p class="section-desc">Early tenure customers are the most vulnerable to churn</p>'
                f'</div><span class="section-tag" style="background:{COLORS.SUCCESS_LT};color:#166534">Retention Opportunity</span></div>',
                unsafe_allow_html=True)
    dsh = dashboard.copy()
    dsh['tg'] = pd.cut(dsh['Tenure'], bins=[0,6,12,24,36,72], labels=['0-6m','7-12m','13-24m','25-36m','37-72m'])
    td = dsh.groupby('tg', observed=True)['churn_probability'].mean()
    st_echarts({
        "backgroundColor": ECHART_BG,
        "tooltip": {"trigger": "axis"},
        "xAxis": {"type": "category", "data": td.index.tolist(), "axisLabel": ax_label_b(), "axisLine": ax_line(),
                  "name": "Tenure Group", "nameLocation": "middle", "nameGap": 28, "nameTextStyle": name_style()},
        "yAxis": {"type": "value", "axisLabel": ax_label(), "splitLine": sp_line(),
                  "name": "Avg Churn Probability", "nameLocation": "middle", "nameGap": 46, "nameTextStyle": name_style()},
        "series": [{"type": "line", "data": [round(safe_val(v), 4) for v in td.values],
                    "smooth": True, "lineStyle": {"color": C_PRIMARY, "width": 3},
                    "areaStyle": {"color": "rgba(5,102,141,0.08)"},
                    "itemStyle": {"color": C_PRIMARY},
                    "markPoint": {"data": [{"type": "max", "name": "Peak"}], "itemStyle": {"color": C_RED}}}],
        "grid": {"left": "10%", "right": "4%", "top": "10%", "bottom": "16%"}
    }, height="240px")
    st.markdown(f'<div class="insight">{get_tenure_insight(dashboard)}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# =============================================================================
# PAGE 5 — SEGMENTS
# =============================================================================
elif page == "Segments":
    st.markdown("""<div class="page-header"><div>
        <p class="page-title">Customer Segments</p>
        <p class="page-subtitle">Cross-dimensional breakdown of churn risk across key customer attributes</p>
        </div><span class="page-badge">Deep Dive</span></div>""", unsafe_allow_html=True)

    risk_counts = dashboard['risk_level'].value_counts()
    st.markdown(f"""<div style='display:flex;gap:10px;flex-wrap:wrap;margin-bottom:{SPACING.S5}'>
        <div class='stat-pill'>Total <b>{kpis['total']:,}</b></div>
        <div class='stat-pill'>High+Critical <b>{int(risk_counts.get('High',0))+int(risk_counts.get('Critical',0)):,}</b></div>
        <div class='stat-pill'>Avg Prob <b>{kpis['avg_prob']:.1%}</b></div>
        <div class='stat-pill'>OOF AUC <b>{kpis['oof_auc']:.3f}</b></div>
    </div>""", unsafe_allow_html=True)

    c1, c2 = st.columns(2)

    with c1:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-header"><div>'
                    '<p class="section-title">Contract × Internet Service</p>'
                    '<p class="section-desc">Average churn probability by contract and service type</p>'
                    '</div></div>', unsafe_allow_html=True)
        pivot = dashboard.pivot_table(values='churn_probability', index='Contract', columns='InternetService', aggfunc='mean').round(3).fillna(0)
        fig_h = go.Figure(go.Heatmap(
            z=pivot.values.tolist(), x=pivot.columns.tolist(), y=pivot.index.tolist(),
            colorscale=[[0, COLORS.PRIMARY_50],[0.5, COLORS.PRIMARY_600],[1, COLORS.PRIMARY_800]],
            text=[[f"{v:.1%}" for v in row] for row in pivot.values],
            texttemplate='%{text}', showscale=True, textfont={"size": 12}))
        fig_h.update_layout(
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            font=dict(family=FONT, size=11), margin=dict(t=8,b=8,l=8,r=8), height=220)
        st.plotly_chart(fig_h, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with c2:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-header"><div>'
                    '<p class="section-title">Risk Level by Senior Citizen</p>'
                    '<p class="section-desc">Churn risk distribution for senior vs non-senior customers</p>'
                    '</div></div>', unsafe_allow_html=True)
        if 'SeniorCitizen' in dashboard.columns:
            sc_data = dashboard.groupby(['SeniorCitizen','risk_level']).size().unstack(fill_value=0)
            sc_data.index = ['Non-Senior','Senior']
            series = []
            for col in sc_data.columns:
                series.append({
                    "name": col, "type": "bar", "stack": "total",
                    "data": [safe_val(v) for v in sc_data[col].tolist()],
                    "itemStyle": {"color": RISK_COLORS.get(col, COLORS.SLATE_300)},
                    "label": {"show": True, "formatter": "{c}", "fontSize": 10}
                })
            st_echarts({
                "backgroundColor": ECHART_BG,
                "tooltip": {"trigger": "axis", "axisPointer": {"type": "shadow"}},
                "legend": {"data": sc_data.columns.tolist(), "bottom": 0, "textStyle": {"fontSize": 11, "color": C_BODY}},
                "xAxis": {"type": "category", "data": ["Non-Senior","Senior"],
                          "axisLabel": {**ax_label_b(), "fontSize": 12}, "axisLine": ax_line()},
                "yAxis": {"type": "value", "axisLabel": ax_label(), "splitLine": sp_line()},
                "series": series,
                "grid": {"left": "8%", "right": "4%", "top": "8%", "bottom": "18%"}
            }, height="240px")
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
    c3, c4 = st.columns(2)

    with c3:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-header"><div>'
                    '<p class="section-title">Monthly Charges by Risk Level</p>'
                    '<p class="section-desc">Do higher-paying customers churn more?</p>'
                    '</div></div>', unsafe_allow_html=True)
        mc_risk = dashboard.groupby('risk_level', observed=True)['MonthlyCharges'].mean().reindex(['Low','Medium','High','Critical'])
        st_echarts({
            "backgroundColor": ECHART_BG,
            "tooltip": {"trigger": "axis"},
            "xAxis": {"type": "category", "data": mc_risk.index.tolist(), "axisLabel": ax_label_b(), "axisLine": ax_line()},
            "yAxis": {"type": "value", "axisLabel": {**ax_label(), "formatter": "${value}"}, "splitLine": sp_line()},
            "series": [{"type": "bar",
                        "data": [{"value": round(safe_val(v), 2), "itemStyle": {"color": RISK_COLORS[k], "borderRadius": [4,4,0,0]}}
                                 for k, v in zip(mc_risk.index, mc_risk.values)],
                        "label": {"show": True, "position": "top", "formatter": "${c}", "color": C_BODY, "fontSize": 11}}],
            "grid": {"left": "8%", "right": "4%", "top": "16%", "bottom": "10%"}
        }, height="240px")
        avg_high = safe_val(mc_risk.get('High', 0))
        avg_low  = safe_val(mc_risk.get('Low',  0))
        st.markdown(f'<div class="insight">High-risk customers pay <b>${avg_high:.2f}/mo</b> vs <b>${avg_low:.2f}/mo</b> '
                    f'for low-risk — a <b>${avg_high-avg_low:.2f}</b> gap. Higher charges correlate with dissatisfaction, not loyalty.</div>',
                    unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with c4:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-header"><div>'
                    '<p class="section-title">Avg Tenure by Contract & Risk</p>'
                    '<p class="section-desc">Longer tenure customers are more committed</p>'
                    '</div></div>', unsafe_allow_html=True)
        tenure_data = (dashboard.groupby(['Contract','risk_level'], observed=True)['Tenure']
                       .mean().unstack(fill_value=0)
                       .reindex(columns=['Low','Medium','High','Critical']).fillna(0))
        series_t = []
        for col in tenure_data.columns:
            if col in RISK_COLORS:
                series_t.append({
                    "name": col, "type": "bar",
                    "data": [round(safe_val(v), 1) for v in tenure_data[col].values],
                    "itemStyle": {"color": RISK_COLORS[col], "borderRadius": [3,3,0,0]}
                })
        st_echarts({
            "backgroundColor": ECHART_BG,
            "tooltip": {"trigger": "axis"},
            "legend": {"data": ['Low','Medium','High','Critical'], "bottom": 0, "textStyle": {"fontSize": 10, "color": C_BODY}},
            "xAxis": {"type": "category", "data": tenure_data.index.tolist(),
                      "axisLabel": {**ax_label_b(), "fontSize": 10}, "axisLine": ax_line()},
            "yAxis": {"type": "value", "axisLabel": ax_label(), "splitLine": sp_line(),
                      "name": "Avg Tenure (mo)", "nameLocation": "middle", "nameGap": 40, "nameTextStyle": name_style()},
            "series": series_t,
            "grid": {"left": "12%", "right": "4%", "top": "8%", "bottom": "18%"}
        }, height="240px")
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-header"><div>'
                '<p class="section-title">Segment Summary Table</p>'
                '<p class="section-desc">All key metrics by contract type and internet service</p>'
                '</div></div>', unsafe_allow_html=True)
    seg = dashboard.groupby(['Contract','InternetService']).agg(
        Customers=('id','count'),
        Avg_Churn_Prob=('churn_probability','mean'),
        Avg_Monthly=('MonthlyCharges','mean'),
        Avg_Tenure=('Tenure','mean'),
        High_Risk=('risk_level', lambda x: (x.isin(['High','Critical'])).sum())
    ).reset_index()
    seg['Avg Churn Prob'] = seg['Avg_Churn_Prob'].apply(lambda x: f'{x:.1%}')
    seg['Avg Monthly']    = seg['Avg_Monthly'].apply(lambda x: f'${x:.2f}')
    seg['Avg Tenure']     = seg['Avg_Tenure'].apply(lambda x: f'{x:.0f} mo')
    seg['High Risk %']    = (seg['High_Risk'] / seg['Customers'] * 100).apply(lambda x: f'{x:.1f}%')
    display_seg = seg[['Contract','InternetService','Customers','Avg Churn Prob','Avg Monthly','Avg Tenure','High Risk %']]
    st.dataframe(display_seg, use_container_width=True, hide_index=True)
    st.markdown('</div>', unsafe_allow_html=True)
