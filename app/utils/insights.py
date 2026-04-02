import pandas as pd
import numpy as np

def get_overview_insights(df: pd.DataFrame, kpis: dict) -> str:
    at_risk_pct = kpis['at_risk_pct']
    high_risk   = kpis['high_risk']
    total       = kpis['total']
    if at_risk_pct > 50:
        urgency = "critical — more than half the customer base shows churn signals"
    elif at_risk_pct > 30:
        urgency = "high — a significant portion of customers are at risk"
    else:
        urgency = "moderate — churn risk is concentrated in a smaller segment"
    return (
        f"Churn risk level is <b>{urgency}</b>. "
        f"{high_risk:,} customers ({high_risk/total:.1%}) have a predicted churn probability above 50% "
        f"and require immediate retention action."
    )

def get_contract_insight(df: pd.DataFrame) -> str:
    rates = df.groupby('Contract')['churn_probability'].mean()
    highest = rates.idxmax()
    lowest  = rates.idxmin()
    gap     = rates.max() - rates.min()
    count_highest = len(df[df['Contract'] == highest])
    return (
        f"<b>{highest}</b> customers have the highest average churn probability "
        f"({rates.max():.1%}), which is <b>{gap:.1%} higher</b> than <b>{lowest}</b> customers "
        f"({rates.min():.1%}). There are {count_highest:,} {highest} customers "
        f"in this dataset — converting even 20% to annual plans could significantly reduce churn."
    )

def get_internet_insight(df: pd.DataFrame) -> str:
    rates   = df.groupby('InternetService')['churn_probability'].mean()
    highest = rates.idxmax()
    lowest  = rates.idxmin()
    count   = len(df[df['InternetService'] == highest])
    avg_charge = df[df['InternetService'] == highest]['MonthlyCharges'].mean()
    return (
        f"<b>{highest}</b> customers show the highest churn risk ({rates.max():.1%}), "
        f"despite paying an average of <b>${avg_charge:.2f}/month</b>. "
        f"This suggests price-to-value perception issues. "
        f"{count:,} customers are affected. "
        f"<b>{lowest}</b> customers are the most loyal ({rates.min():.1%} churn risk)."
    )

def get_payment_insight(df: pd.DataFrame) -> str:
    rates   = df.groupby('PaymentMethod')['churn_probability'].mean()
    highest = rates.idxmax()
    lowest  = rates.idxmin()
    count   = len(df[df['PaymentMethod'] == highest])
    auto_methods   = [m for m in rates.index if 'automatic' in m.lower()]
    manual_methods = [m for m in rates.index if 'automatic' not in m.lower()]
    if auto_methods and manual_methods:
        auto_avg   = rates[auto_methods].mean()
        manual_avg = rates[manual_methods].mean()
        auto_msg   = (
            f"Automatic payment customers average {auto_avg:.1%} churn risk vs "
            f"{manual_avg:.1%} for manual payment customers. "
        )
    else:
        auto_msg = ""
    return (
        f"<b>{highest}</b> has the highest churn risk ({rates.max():.1%}) with {count:,} customers. "
        f"{auto_msg}"
        f"Encouraging enrollment in automatic payments could reduce churn — "
        f"<b>{lowest}</b> customers ({rates.min():.1%} risk) are the most loyal segment."
    )

def get_tenure_insight(df: pd.DataFrame) -> str:
    df = df.copy()
    df['tenure_group'] = pd.cut(
        df['Tenure'],
        bins=[0, 6, 12, 24, 36, 72],
        labels=['0-6m', '7-12m', '13-24m', '25-36m', '37-72m']
    )
    rates   = df.groupby('tenure_group', observed=True)['churn_probability'].mean()
    highest = rates.idxmax()
    drop    = rates.max() - rates.min()
    early_count = len(df[df['Tenure'] <= 12])
    early_pct   = early_count / len(df) * 100
    return (
        f"The <b>{highest}</b> tenure group shows the highest churn risk ({rates.max():.1%}). "
        f"Churn risk drops by <b>{drop:.1%}</b> between the earliest and latest tenure groups. "
        f"{early_count:,} customers ({early_pct:.1f}%) are in their first 12 months — "
        f"the most vulnerable window. A structured onboarding program targeting this group "
        f"could have the highest retention ROI."
    )

def get_customer_risk_insight(df_filtered: pd.DataFrame, df_total: pd.DataFrame) -> str:
    if len(df_filtered) == 0:
        return "No customers match the selected filters. Try adjusting the criteria."
    pct_of_total = len(df_filtered) / len(df_total) * 100
    avg_prob     = df_filtered['churn_probability'].mean()
    avg_charge   = df_filtered['MonthlyCharges'].mean()
    top_contract = df_filtered['Contract'].value_counts().idxmax()
    top_internet = df_filtered['InternetService'].value_counts().idxmax()
    return (
        f"The current filter shows <b>{len(df_filtered):,} customers</b> "
        f"({pct_of_total:.1f}% of total) with an average churn probability of <b>{avg_prob:.1%}</b>. "
        f"The dominant profile is <b>{top_contract}</b> contract with <b>{top_internet}</b> internet, "
        f"paying an average of <b>${avg_charge:.2f}/month</b>. "
        f"Focus retention efforts on this segment first."
    )

def get_model_insight(auc: float) -> str:
    if auc >= 0.90:
        quality = "excellent"
        action  = "The model can be used with high confidence for customer targeting."
    elif auc >= 0.85:
        quality = "very good"
        action  = "The model is reliable for prioritizing retention campaigns."
    elif auc >= 0.80:
        quality = "good"
        action  = "The model provides meaningful signal for churn detection."
    else:
        quality = "acceptable"
        action  = "The model provides directional guidance but should be used carefully."
    return (
        f"The model achieves an OOF AUC of <b>{auc:.3f}</b>, which is considered <b>{quality}</b> "
        f"for churn prediction in telecommunications. {action} "
        f"OOF (Out-of-Fold) evaluation ensures there is no data leakage — "
        f"every prediction was made on customers the model had never seen during training."
    )
