import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from sklearn.metrics import roc_curve, confusion_matrix

from utils.data_loader import RISK_COLORS, RISK_ORDER

# ── Color palette ──────────────────────────────────────────────────────────────
PRIMARY  = '#1f3b73'
ACCENT   = '#FF8C00'
BG_COLOR = '#FFFFFF'
GRAY     = '#f8f9fa'

# ── Chart defaults ─────────────────────────────────────────────────────────────
LAYOUT = dict(
    paper_bgcolor = BG_COLOR,
    plot_bgcolor  = BG_COLOR,
    font          = dict(family='Inter, sans-serif', color='#2c3e50', size=12),
    margin        = dict(t=40, b=40, l=40, r=40),
)

# ── Charts ─────────────────────────────────────────────────────────────────────
def churn_risk_histogram(df: pd.DataFrame) -> go.Figure:
    fig = px.histogram(
        df, x='churn_probability', nbins=40,
        color_discrete_sequence=[PRIMARY],
        title='Churn Risk Distribution'
    )
    fig.add_vline(x=0.25, line_dash='dash', line_color=ACCENT,
                  annotation_text='Medium risk', annotation_position='top right')
    fig.add_vline(x=0.50, line_dash='dash', line_color='#e74c3c',
                  annotation_text='High risk', annotation_position='top right')
    fig.update_layout(**LAYOUT)
    fig.update_layout(xaxis_title='Churn Probability', yaxis_title='Customers')
    return fig


def risk_level_bar(df: pd.DataFrame) -> go.Figure:
    counts = df['risk_level'].value_counts().reindex(RISK_ORDER).fillna(0)
    fig = go.Figure(go.Bar(
        x=counts.index.tolist(),
        y=counts.values,
        marker_color=[RISK_COLORS[r] for r in counts.index],
        text=counts.values,
        textposition='outside'
    ))
    fig.update_layout(**LAYOUT)
    fig.update_layout(
        title='Customers by Risk Level',
        xaxis_title='Risk Level',
        yaxis_title='Customers'
    )
    return fig


def churn_by_segment(df: pd.DataFrame, col: str) -> go.Figure:
    rates = df.groupby(col)['churn_probability'].mean().sort_values(ascending=False)
    fig = go.Figure(go.Bar(
        x=rates.values,
        y=rates.index.astype(str),
        orientation='h',
        marker_color=PRIMARY,
        text=[f'{v:.1%}' for v in rates.values],
        textposition='outside'
    ))
    fig.add_vline(x=df['churn_probability'].mean(),
                  line_dash='dash', line_color=ACCENT,
                  annotation_text='Average')
    fig.update_layout(**LAYOUT)
    fig.update_layout(
        title=f'Avg Churn Probability by {col}',
        xaxis_title='Avg Churn Probability',
        yaxis_title=col,
        height=400
    )
    return fig


def oof_distribution(oof: pd.DataFrame) -> go.Figure:
    fig = go.Figure()
    for label, color, name in [(0, PRIMARY, 'No Churn'), (1, ACCENT, 'Churn')]:
        data = oof[oof['Churn_real'] == label]['Churn_pred']
        fig.add_trace(go.Histogram(
            x=data, nbinsx=40, name=name,
            marker_color=color, opacity=0.7,
            histnorm='probability density'
        ))
    fig.add_vline(x=0.5, line_dash='dash', line_color='#e74c3c')
    fig.update_layout(**LAYOUT)
    fig.update_layout(
        title='OOF Predictions Distribution',
        xaxis_title='Predicted Churn Probability',
        yaxis_title='Density',
        barmode='overlay',
        legend=dict(x=0.7, y=0.95)
    )
    return fig


def roc_curve_plot(oof: pd.DataFrame) -> go.Figure:
    fpr, tpr, _ = roc_curve(oof['Churn_real'], oof['Churn_pred'])
    from sklearn.metrics import roc_auc_score
    auc = roc_auc_score(oof['Churn_real'], oof['Churn_pred'])

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=fpr, y=tpr, mode='lines',
        line=dict(color=PRIMARY, width=2),
        name=f'ROC Curve (AUC = {auc:.3f})'
    ))
    fig.add_trace(go.Scatter(
        x=[0, 1], y=[0, 1], mode='lines',
        line=dict(color='gray', width=1, dash='dash'),
        name='Random (AUC = 0.5)'
    ))
    fig.update_layout(**LAYOUT)
    fig.update_layout(
        title='ROC Curve',
        xaxis_title='False Positive Rate',
        yaxis_title='True Positive Rate',
        legend=dict(x=0.5, y=0.1)
    )
    return fig


def confusion_matrix_plot(oof: pd.DataFrame, threshold: float = 0.5) -> go.Figure:
    y_pred = (oof['Churn_pred'] >= threshold).astype(int)
    cm = confusion_matrix(oof['Churn_real'], y_pred)
    labels = ['No Churn', 'Churn']

    fig = go.Figure(go.Heatmap(
        z=cm,
        x=[f'Predicted {l}' for l in labels],
        y=[f'Actual {l}' for l in labels],
        colorscale=[[0, '#f8f9fa'], [1, PRIMARY]],
        text=cm, texttemplate='%{text}',
        showscale=False
    ))
    fig.update_layout(**LAYOUT)
    fig.update_layout(title=f'Confusion Matrix (threshold={threshold:.2f})')
    return fig