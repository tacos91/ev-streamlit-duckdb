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

# ===== Navigation ajoutée =====
st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Navigation",
    ["Dashboard", "À propos du projet"]
)

# ==============================
# CONTENU PRINCIPAL
# ==============================
st.title("📊 Application d’Analyse Multi-Datasets")
st.markdown("---")

if page == "Dashboard":
    if dataset == "Ventes Walmart":
        run_walmart_dashboard()
    else:
        run_ev_dashboard()

elif page == "À propos du projet":
    st.title("📘 À propos du projet")

    st.markdown("""
    ## 🎯 Objectif du projet

    Cette application a été développée dans le cadre du MBA ESG – Management Opérationnel.

    Elle permet :
    - L’analyse multi-datasets
    - Le calcul de KPI via SQL (DuckDB)
    - La visualisation interactive avec Streamlit
    - L’aide à la décision basée sur les données

    ---

    ## 👥 Organisation de l'équipe

    🧑‍💼 **Chef de projet**  
    Ines Taibi  

    👨‍💻 **Développeur principal**  
    Mathis KODIA  

    👩‍💻 **Développeur**  
    Myriam  bennani

    🧪 **Test & QA**  
    Aghilas Aissaoui  

    ---

    ## 🏗️ Architecture

    - app.py : Routing principal  
    - analytics/ : Logique métier  
    - DuckDB : Requêtes SQL en mémoire  
    - Plotly : Visualisations interactives  
    """)