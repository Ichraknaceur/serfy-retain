import os

import requests
import streamlit as st

PRODUCT_NAME = os.getenv("PRODUCT_NAME", "Serfy Retain")
API_URL = os.getenv("API_URL", "http://localhost:8000")

st.set_page_config(page_title=PRODUCT_NAME, layout="wide")

st.markdown(
    """
    <style>
    .stApp {
        background:
            radial-gradient(circle at top left, rgba(0, 122, 102, 0.12), transparent 32%),
            radial-gradient(circle at top right, rgba(194, 155, 77, 0.14), transparent 28%),
            #f7f4ee;
    }
    .hero {
        padding: 2rem;
        border-radius: 24px;
        background: linear-gradient(135deg, #0f3d3a 0%, #195851 100%);
        color: #f8f4ec;
        box-shadow: 0 18px 50px rgba(15, 61, 58, 0.18);
    }
    .hero h1 {
        color: #f8f4ec;
        font-size: 3rem;
        margin-bottom: 0.3rem;
    }
    .hero p {
        font-size: 1.05rem;
        color: rgba(248, 244, 236, 0.9);
    }
    .panel {
        background: rgba(255, 255, 255, 0.8);
        border: 1px solid rgba(15, 61, 58, 0.08);
        border-radius: 20px;
        padding: 1.2rem;
        min-height: 180px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    f"""
    <div class="hero">
        <h1>{PRODUCT_NAME}</h1>
        <p>AI-powered retention intelligence for retail banking.</p>
        <p>Cette nouvelle base sert a construire proprement la prediction churn, les offres de retention et les parcours de suivi client.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.write("")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(
        """
        <div class="panel">
            <h3>Produit</h3>
            <p>Une plateforme qui detecte les clients a risque et aide la banque a agir avant le depart.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col2:
    st.markdown(
        """
        <div class="panel">
            <h3>Architecture</h3>
            <p>Backend FastAPI, frontend Streamlit, monitoring separe et modules metier a brancher progressivement.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col3:
    st.markdown(
        """
        <div class="panel">
            <h3>Priorites</h3>
            <p>Modele churn, recommandations d'offres, agent IA, feedback humain et observabilite.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.write("")
st.subheader("Etat de l'API")

try:
    response = requests.get(f"{API_URL}/health", timeout=3)
    response.raise_for_status()
    st.success(f"Backend disponible: {response.json()}")
except Exception as exc:
    st.warning(f"Backend non joignable pour le moment: {exc}")

st.subheader("Roadmap propre")
st.markdown(
    """
    1. Stabiliser le schema client et les features d'entree.
    2. Ajouter le service de prediction churn.
    3. Construire le moteur de recommandation d'offres.
    4. Ajouter la personnalisation IA avec garde-fous.
    5. Integrer monitoring, evaluation et boucle de feedback.
    """
)
