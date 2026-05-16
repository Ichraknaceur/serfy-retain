import os
from typing import Any, Dict, Optional

import requests
import streamlit as st

PRODUCT_NAME = os.getenv("PRODUCT_NAME", "Serfy Retain")
API_URL = os.getenv("API_URL", "http://localhost:8000")
TIMEOUT_SECONDS = 8

DEFAULT_CUSTOMER = {
    "customer_age": 45,
    "gender": "M",
    "dependent_count": 2,
    "education_level": "Graduate",
    "marital_status": "Married",
    "income_category": "$60K - $80K",
    "card_category": "Blue",
    "months_on_book": 36,
    "total_relationship_count": 4,
    "months_inactive_12_mon": 2,
    "contacts_count_12_mon": 3,
    "credit_limit": 10000.0,
    "total_revolving_bal": 1500.0,
    "avg_open_to_buy": 8500.0,
    "total_amt_chng_q4_q1": 1.5,
    "total_trans_amt": 5000.0,
    "total_trans_ct": 50,
    "total_ct_chng_q4_q1": 1.2,
    "avg_utilization_ratio": 0.15,
}

EDUCATION_OPTIONS = [
    "Uneducated",
    "High School",
    "College",
    "Graduate",
    "Post-Graduate",
    "Doctorate",
    "Unknown",
]
MARITAL_OPTIONS = ["Single", "Married", "Divorced", "Unknown"]
INCOME_OPTIONS = [
    "Less than $40K",
    "$40K - $60K",
    "$60K - $80K",
    "$80K - $120K",
    "$120K +",
    "Unknown",
]
CARD_OPTIONS = ["Blue", "Silver", "Gold", "Platinum"]
GENDER_OPTIONS = ["M", "F"]

st.set_page_config(page_title=PRODUCT_NAME, page_icon="/", layout="wide")

st.markdown(
    """
    <style>
    :root {
        --bg: #f7f1e8;
        --panel: #fffdfa;
        --panel-soft: #fcf8f1;
        --ink: #183430;
        --muted: #667b74;
        --line: rgba(24, 52, 48, 0.10);
        --green: #184b46;
        --green-2: #2a655d;
        --green-soft: #e7f5ef;
        --amber-soft: #fff1dc;
        --amber-ink: #9c6615;
        --red-soft: #fde8e4;
        --red-ink: #a64133;
        --shadow: 0 20px 48px rgba(24, 52, 48, 0.08);
        --radius: 24px;
    }

    .stApp {
        background:
            radial-gradient(circle at top left, rgba(42, 101, 93, 0.10), transparent 28%),
            radial-gradient(circle at top right, rgba(198, 161, 95, 0.16), transparent 24%),
            var(--bg);
    }

    html, body, [class*="css"], p, li, label, div, span {
        color: var(--ink);
    }

    .block-container {
        max-width: 1320px;
        padding-top: 1.2rem;
        padding-bottom: 2.4rem;
    }

    h1, h2, h3 {
        color: var(--ink) !important;
        letter-spacing: -0.02em;
    }

    .hero {
        background:
            radial-gradient(circle at 88% 12%, rgba(255,255,255,0.14), transparent 20%),
            linear-gradient(135deg, #173f3a 0%, #265e57 100%);
        border-radius: 32px;
        padding: 2rem 2.1rem;
        box-shadow: 0 28px 58px rgba(23, 63, 58, 0.18);
        margin-bottom: 1.2rem;
    }

    .hero-grid {
        display: grid;
        grid-template-columns: 1.25fr 0.75fr;
        gap: 1rem;
        align-items: end;
    }

    .hero h1 {
        color: #f8f4ee !important;
        font-size: 2.7rem;
        margin: 0 0 0.4rem 0;
    }

    .hero p {
        color: rgba(248, 244, 238, 0.92);
        margin: 0.25rem 0;
        max-width: 900px;
    }

    .hero-badges {
        display: flex;
        gap: 0.55rem;
        flex-wrap: wrap;
        justify-content: flex-end;
    }

    .badge {
        display: inline-block;
        padding: 0.45rem 0.78rem;
        border-radius: 999px;
        font-size: 0.84rem;
        font-weight: 700;
        background: rgba(255,255,255,0.14);
        color: #f8f4ee;
        border: 1px solid rgba(255,255,255,0.16);
    }

    .summary-card, .decision-card, .mini-card {
        background: var(--panel);
        border: 1px solid var(--line);
        border-radius: var(--radius);
        box-shadow: var(--shadow);
    }

    .summary-card {
        padding: 1.05rem 1.15rem;
        min-height: 150px;
    }

    .summary-label {
        color: var(--muted);
        text-transform: uppercase;
        font-size: 0.81rem;
        letter-spacing: 0.06em;
        margin-bottom: 0.7rem;
    }

    .summary-value {
        font-size: 1.95rem;
        font-weight: 780;
        line-height: 1.05;
        color: var(--ink);
    }

    .summary-meta {
        color: var(--muted);
        font-size: 0.94rem;
        margin-top: 0.42rem;
    }

    .status-pill {
        display: inline-block;
        padding: 0.35rem 0.72rem;
        border-radius: 999px;
        font-size: 0.83rem;
        font-weight: 700;
        margin-bottom: 0.75rem;
    }

    .good { background: var(--green-soft); color: #1f6d42; }
    .warn { background: var(--amber-soft); color: var(--amber-ink); }
    .bad { background: var(--red-soft); color: var(--red-ink); }

    .section-note {
        color: var(--muted);
        margin-top: -0.15rem;
        margin-bottom: 0.85rem;
        font-size: 0.96rem;
    }

    .form-shell {
        background: var(--panel);
        border: 1px solid var(--line);
        border-radius: 26px;
        padding: 1rem 1rem 0.3rem 1rem;
        box-shadow: var(--shadow);
    }

    .form-section {
        background: var(--panel-soft);
        border: 1px solid var(--line);
        border-radius: 18px;
        padding: 0.95rem 0.95rem 0.35rem 0.95rem;
        margin-bottom: 0.9rem;
    }

    .form-section-title {
        font-size: 0.8rem;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        color: var(--muted);
        margin-bottom: 0.6rem;
    }

    .form-hint {
        color: var(--muted);
        font-size: 0.88rem;
        margin-top: -0.25rem;
        margin-bottom: 0.7rem;
    }

    .decision-card {
        padding: 1.35rem;
        background: linear-gradient(180deg, #fffdfa 0%, #f8f2e8 100%);
    }

    .decision-title {
        font-size: 0.83rem;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        color: var(--muted);
    }

    .decision-score {
        font-size: 3.15rem;
        line-height: 1;
        font-weight: 830;
        color: var(--ink);
        margin: 0.55rem 0 0.7rem 0;
    }

    .decision-grid {
        display: grid;
        grid-template-columns: repeat(2, minmax(0, 1fr));
        gap: 0.8rem;
        margin-top: 1rem;
    }

    .decision-box {
        background: #ffffff;
        border: 1px solid var(--line);
        border-radius: 18px;
        padding: 0.9rem;
    }

    .decision-box .label {
        font-size: 0.78rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        color: var(--muted);
        margin-bottom: 0.35rem;
    }

    .decision-box .value {
        font-size: 1.03rem;
        font-weight: 740;
        color: var(--ink);
    }

    .action-box {
        margin-top: 1rem;
        padding: 1rem;
        border-radius: 18px;
        border: 1px solid var(--line);
        background: rgba(255,255,255,0.82);
    }

    .action-box h4 {
        margin: 0 0 0.3rem 0;
        color: var(--ink);
    }

    .mini-card {
        padding: 1rem;
        min-height: 150px;
    }

    div[data-testid="stForm"] {
        background: transparent;
        border: none;
        padding: 0;
        box-shadow: none;
    }

    div[data-testid="stNumberInputContainer"],
    div[data-testid="stSelectbox"] > div,
    div[data-baseweb="select"] > div,
    div[data-baseweb="input"] > div {
        background: #ffffff !important;
        border: 1px solid rgba(24, 52, 48, 0.14) !important;
        border-radius: 14px !important;
        box-shadow: none !important;
    }

    div[data-testid="stNumberInputContainer"] input,
    div[data-baseweb="select"] *,
    div[data-baseweb="input"] input,
    .stNumberInput input,
    .stSelectbox div[data-baseweb="select"] {
        color: var(--ink) !important;
        background: transparent !important;
    }

    div[data-testid="stNumberInputContainer"] button,
    div[data-baseweb="select"] svg {
        color: var(--green) !important;
        fill: var(--green) !important;
    }

    label, .stSelectbox label, .stNumberInput label {
        color: var(--ink) !important;
        font-weight: 640 !important;
    }

    .stButton > button,
    .stFormSubmitButton > button {
        background: linear-gradient(135deg, var(--green) 0%, var(--green-2) 100%);
        color: white;
        border: none;
        border-radius: 14px;
        font-weight: 720;
        min-height: 2.95rem;
        padding: 0 1rem;
    }

    .stButton > button:hover,
    .stFormSubmitButton > button:hover {
        color: white;
        background: linear-gradient(135deg, #153f3a 0%, #23564f 100%);
    }

    .stTabs [data-baseweb="tab-list"] {
        gap: 0.5rem;
    }

    .stTabs [data-baseweb="tab"] {
        background: rgba(255,255,255,0.72);
        border-radius: 999px;
        padding: 0.45rem 0.9rem;
        border: 1px solid var(--line);
    }

    @media (max-width: 980px) {
        .hero-grid,
        .decision-grid {
            grid-template-columns: 1fr;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)


def fetch_json(endpoint: str) -> tuple[Optional[Dict[str, Any]], Optional[str]]:
    try:
        response = requests.get(f"{API_URL}{endpoint}", timeout=TIMEOUT_SECONDS)
        response.raise_for_status()
        return response.json(), None
    except Exception as exc:
        return None, str(exc)


@st.cache_data(ttl=20)
def get_health() -> tuple[Optional[Dict[str, Any]], Optional[str]]:
    return fetch_json("/health")


@st.cache_data(ttl=20)
def get_model_info() -> tuple[Optional[Dict[str, Any]], Optional[str]]:
    return fetch_json("/model-info")


def risk_badge(risk: str) -> str:
    if risk == "high":
        return '<span class="status-pill bad">High churn risk</span>'
    if risk == "medium":
        return '<span class="status-pill warn">Medium churn risk</span>'
    return '<span class="status-pill good">Low churn risk</span>'


def status_badge(ok: bool) -> str:
    return '<span class="status-pill good">Backend online</span>' if ok else '<span class="status-pill bad">Backend unavailable</span>'


def recommended_action(risk: str) -> tuple[str, str, str]:
    if risk == "high":
        return (
            "Priority retention follow-up",
            "Escalate this profile into the retention workflow with proactive outreach, tailored offer review, and advisor contact.",
            "High-priority watchlist",
        )
    if risk == "medium":
        return (
            "Targeted advisor review",
            "Review the profile for early warning signs and consider a light-touch retention action before churn risk rises further.",
            "Monitor closely",
        )
    return (
        "Standard servicing posture",
        "This profile looks stable for now. No urgent intervention is required beyond regular service and periodic review.",
        "Routine follow-up",
    )


def business_segment(risk: str) -> str:
    return {
        "high": "Immediate retention candidate",
        "medium": "Watchlist candidate",
        "low": "Stable relationship",
    }.get(risk, "Stable relationship")


health_data, health_error = get_health()
model_info, model_info_error = get_model_info()
metrics = model_info.get("metrics", {}) if model_info else {}

st.markdown(
    f"""
    <div class="hero">
        <div class="hero-grid">
            <div>
                <h1>{PRODUCT_NAME}</h1>
                <p>Advisor-facing workspace for churn prevention and retention prioritization.</p>
                <p>Score a client profile, review the likelihood of churn, and translate the result into a business-ready next step.</p>
            </div>
            <div class="hero-badges">
                <span class="badge">Artifact-backed scoring</span>
                <span class="badge">Advisor workflow</span>
                <span class="badge">MLflow tracked</span>
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

kpi_1, kpi_2, kpi_3 = st.columns(3)

with kpi_1:
    if health_data:
        st.markdown(
            f"""
            <div class="summary-card">
                <div class="summary-label">Platform readiness</div>
                {status_badge(True)}
                <div class="summary-value" style="font-size:1.35rem;">Scoring service ready</div>
                <div class="summary-meta">Environment: {health_data.get('environment', 'unknown')}</div>
                <div class="summary-meta">Artifacts available: {health_data.get('model_artifacts_ready', False)}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            f"""
            <div class="summary-card">
                <div class="summary-label">Platform readiness</div>
                {status_badge(False)}
                <div class="summary-value" style="font-size:1.35rem;">Connection issue</div>
                <div class="summary-meta">{health_error or 'No response received from the backend.'}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

with kpi_2:
    if model_info:
        st.markdown(
            f"""
            <div class="summary-card">
                <div class="summary-label">Active model</div>
                <div class="summary-value">{model_info['model_name']}</div>
                <div class="summary-meta">Transformed features: {model_info['transformed_feature_count']}</div>
                <div class="summary-meta">Ready for production-style inference</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            f"""
            <div class="summary-card">
                <div class="summary-label">Active model</div>
                <div class="summary-value" style="font-size:1.35rem;">Metadata unavailable</div>
                <div class="summary-meta">{model_info_error or 'Model metadata is currently unavailable.'}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

with kpi_3:
    if metrics:
        st.markdown(
            f"""
            <div class="summary-card">
                <div class="summary-label">Validation snapshot</div>
                <div class="summary-value">{metrics.get('roc_auc', 0):.3f}</div>
                <div class="summary-meta">ROC-AUC</div>
                <div class="summary-meta">Accuracy: {metrics.get('accuracy', 0):.3f}</div>
                <div class="summary-meta">F1-score: {metrics.get('f1_score', 0):.3f}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            """
            <div class="summary-card">
                <div class="summary-label">Validation snapshot</div>
                <div class="summary-value" style="font-size:1.35rem;">Metrics unavailable</div>
                <div class="summary-meta">Quality indicators will appear once model metadata is returned by the backend.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

st.write("")
input_col, result_col = st.columns([1.05, 0.95], gap="large")

with input_col:
    st.subheader("Client profile")
    st.markdown(
        '<div class="section-note">Use the grouped form below to score a relationship in a more business-readable way.</div>',
        unsafe_allow_html=True,
    )

    with st.form("prediction_form"):
        st.markdown('<div class="form-shell">', unsafe_allow_html=True)

        st.markdown(
            '<div class="form-section"><div class="form-section-title">Client profile</div><div class="form-hint">Identity, household context, and card positioning.</div>',
            unsafe_allow_html=True,
        )
        a1, a2 = st.columns(2)
        with a1:
            customer_age = st.number_input("Customer age", min_value=18, max_value=120, value=DEFAULT_CUSTOMER["customer_age"], step=1)
            gender = st.selectbox("Gender", GENDER_OPTIONS, index=GENDER_OPTIONS.index(DEFAULT_CUSTOMER["gender"]))
            dependent_count = st.number_input("Dependent count", min_value=0, value=DEFAULT_CUSTOMER["dependent_count"], step=1)
            marital_status = st.selectbox("Marital status", MARITAL_OPTIONS, index=MARITAL_OPTIONS.index(DEFAULT_CUSTOMER["marital_status"]))
        with a2:
            education_level = st.selectbox("Education level", EDUCATION_OPTIONS, index=EDUCATION_OPTIONS.index(DEFAULT_CUSTOMER["education_level"]))
            income_category = st.selectbox("Income category", INCOME_OPTIONS, index=INCOME_OPTIONS.index(DEFAULT_CUSTOMER["income_category"]))
            card_category = st.selectbox("Card category", CARD_OPTIONS, index=CARD_OPTIONS.index(DEFAULT_CUSTOMER["card_category"]))
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown(
            '<div class="form-section"><div class="form-section-title">Relationship with the bank</div><div class="form-hint">Tenure, engagement rhythm, and relationship depth.</div>',
            unsafe_allow_html=True,
        )
        b1, b2 = st.columns(2)
        with b1:
            months_on_book = st.number_input("Months on book", min_value=0, value=DEFAULT_CUSTOMER["months_on_book"], step=1)
            total_relationship_count = st.number_input("Total relationship count", min_value=0, value=DEFAULT_CUSTOMER["total_relationship_count"], step=1)
        with b2:
            months_inactive_12_mon = st.number_input("Inactive months over last 12 months", min_value=0, value=DEFAULT_CUSTOMER["months_inactive_12_mon"], step=1)
            contacts_count_12_mon = st.number_input("Contact count over last 12 months", min_value=0, value=DEFAULT_CUSTOMER["contacts_count_12_mon"], step=1)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown(
            '<div class="form-section"><div class="form-section-title">Credit and transaction behavior</div><div class="form-hint">Capacity, usage, and transaction momentum.</div>',
            unsafe_allow_html=True,
        )
        c1, c2 = st.columns(2)
        with c1:
            credit_limit = st.number_input("Credit limit", min_value=0.0, value=float(DEFAULT_CUSTOMER["credit_limit"]), step=100.0, format="%.2f")
            total_revolving_bal = st.number_input("Total revolving balance", min_value=0.0, value=float(DEFAULT_CUSTOMER["total_revolving_bal"]), step=100.0, format="%.2f")
            avg_open_to_buy = st.number_input("Average open to buy", min_value=0.0, value=float(DEFAULT_CUSTOMER["avg_open_to_buy"]), step=100.0, format="%.2f")
            avg_utilization_ratio = st.number_input(
                "Average utilization ratio",
                min_value=0.0,
                max_value=1.0,
                value=float(DEFAULT_CUSTOMER["avg_utilization_ratio"]),
                step=0.01,
                format="%.2f",
            )
        with c2:
            total_amt_chng_q4_q1 = st.number_input("Transaction amount change Q4/Q1", value=float(DEFAULT_CUSTOMER["total_amt_chng_q4_q1"]), step=0.01, format="%.2f")
            total_trans_amt = st.number_input("Total transaction amount", min_value=0.0, value=float(DEFAULT_CUSTOMER["total_trans_amt"]), step=100.0, format="%.2f")
            total_trans_ct = st.number_input("Total transaction count", min_value=0, value=DEFAULT_CUSTOMER["total_trans_ct"], step=1)
            total_ct_chng_q4_q1 = st.number_input("Transaction count change Q4/Q1", value=float(DEFAULT_CUSTOMER["total_ct_chng_q4_q1"]), step=0.01, format="%.2f")
        st.markdown('</div>', unsafe_allow_html=True)

        submitted = st.form_submit_button("Score customer")
        st.markdown('</div>', unsafe_allow_html=True)

    payload = {
        "customer_age": int(customer_age),
        "gender": gender,
        "dependent_count": int(dependent_count),
        "education_level": education_level,
        "marital_status": marital_status,
        "income_category": income_category,
        "card_category": card_category,
        "months_on_book": int(months_on_book),
        "total_relationship_count": int(total_relationship_count),
        "months_inactive_12_mon": int(months_inactive_12_mon),
        "contacts_count_12_mon": int(contacts_count_12_mon),
        "credit_limit": float(credit_limit),
        "total_revolving_bal": float(total_revolving_bal),
        "avg_open_to_buy": float(avg_open_to_buy),
        "total_amt_chng_q4_q1": float(total_amt_chng_q4_q1),
        "total_trans_amt": float(total_trans_amt),
        "total_trans_ct": int(total_trans_ct),
        "total_ct_chng_q4_q1": float(total_ct_chng_q4_q1),
        "avg_utilization_ratio": float(avg_utilization_ratio),
    }

with result_col:
    st.subheader("Decision output")
    st.markdown(
        '<div class="section-note">The score is translated into business language so the output can support an advisor workflow, not just a technical prediction demo.</div>',
        unsafe_allow_html=True,
    )

    if submitted:
        try:
            response = requests.post(f"{API_URL}/predict", json=payload, timeout=TIMEOUT_SECONDS)
            response.raise_for_status()
            result = response.json()
            action_title, action_copy, follow_up_label = recommended_action(result["risk_level"])

            st.markdown(
                f"""
                <div class="decision-card">
                    <div class="decision-title">Churn probability</div>
                    {risk_badge(result['risk_level'])}
                    <div class="decision-score">{result['churn_probability']:.2%}</div>
                    <div class="section-note" style="margin-bottom:0;">Estimated probability that this client profile will churn according to the active scoring pipeline.</div>
                    <div class="decision-grid">
                        <div class="decision-box">
                            <div class="label">Risk posture</div>
                            <div class="value">{result['risk_level'].upper()}</div>
                        </div>
                        <div class="decision-box">
                            <div class="label">Business segment</div>
                            <div class="value">{business_segment(result['risk_level'])}</div>
                        </div>
                        <div class="decision-box">
                            <div class="label">Follow-up priority</div>
                            <div class="value">{follow_up_label}</div>
                        </div>
                        <div class="decision-box">
                            <div class="label">Scoring model</div>
                            <div class="value">{result['model_name']}</div>
                        </div>
                    </div>
                    <div class="action-box">
                        <h4>{action_title}</h4>
                        <p>{action_copy}</p>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        except requests.HTTPError:
            detail = "Prediction request failed."
            try:
                detail = response.json().get("detail", detail)
            except Exception:
                pass
            st.error(detail)
        except Exception as exc:
            st.error(f"Could not reach the prediction API: {exc}")
    else:
        st.markdown(
            """
            <div class="decision-card">
                <div class="decision-title">Ready for scoring</div>
                <div class="decision-score" style="font-size:2rem;">Awaiting input</div>
                <div class="section-note" style="margin-bottom:0;">Submit a client profile to get a churn score, a business segment, and the recommended servicing posture.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

st.write("")
ops_tab, details_tab = st.tabs(["Advisor workspace", "Technical details"])

with ops_tab:
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(
            """
            <div class="mini-card">
                <div class="summary-label">Primary use</div>
                <div class="summary-value" style="font-size:1.35rem;">Score a relationship</div>
                <div class="summary-meta">Assess whether a client should remain in standard servicing or move toward a retention action.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with c2:
        st.markdown(
            """
            <div class="mini-card">
                <div class="summary-label">Current release</div>
                <div class="summary-value" style="font-size:1.35rem;">Scoring layer</div>
                <div class="summary-meta">This version focuses on reliable churn scoring before recommendations and offers are layered on top.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with c3:
        st.markdown(
            """
            <div class="mini-card">
                <div class="summary-label">Next product step</div>
                <div class="summary-value" style="font-size:1.35rem;">Retention actions</div>
                <div class="summary-meta">The next UI evolution is to add recommended offers and advisor actions beside the score.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

with details_tab:
    left, right = st.columns(2)
    with left:
        st.markdown("### Platform health")
        if health_data:
            st.json(health_data)
        else:
            st.info(health_error or "No health payload available.")

        st.markdown("### Payload example")
        st.json(payload)

    with right:
        st.markdown("### Model details")
        if model_info:
            st.json(
                {
                    "model_name": model_info["model_name"],
                    "target": model_info["target"],
                    "transformed_feature_count": model_info["transformed_feature_count"],
                    "artifacts_dir": model_info["artifacts_dir"],
                    "metrics": model_info.get("metrics", {}),
                }
            )
        else:
            st.info(model_info_error or "Model metadata is not available yet.")
