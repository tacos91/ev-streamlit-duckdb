import streamlit as st
from analytics.walmart_dashboard import run_walmart_dashboard
from analytics.ev_dashboard import run_ev_dashboard

# ==============================
# CONFIGURATION GLOBALE
# ==============================
st.set_page_config(
    page_title="Application d’Analyse Multi-Datasets",
    layout="wide",
    page_icon="📊"
)

# ==============================
# STYLE (léger polish UI)
# ==============================
st.markdown(
    """
    <style>
    .stMetric {
        background-color: #111827;
        padding: 15px;
        border-radius: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ==============================
# SIDEBAR
# ==============================
st.sidebar.title("⚙️ Configuration")

dataset = st.sidebar.selectbox(
    "Sélectionner un jeu de données",
    ["Ventes Walmart", "Véhicules Électriques"]
)

# ===== AJOUT INES (Chef de Projet) =====
st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Navigation",
    ["Dashboard", "À propos du projet"]
)
# =======================================

# ==============================
# CONTENU PRINCIPAL
# ==============================
st.title("📊 Application d’Analyse Multi-Datasets")

st.markdown("---")

# On ne modifie PAS la logique existante
if dataset == "Ventes Walmart":
    run_walmart_dashboard()
else:
    run_ev_dashboard()