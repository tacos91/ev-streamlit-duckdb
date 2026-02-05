import streamlit as st
import pandas as pd

from database.duckdb_manager import store_dataframe
from analytics.kpi_queries import (
    get_brands,
    get_range_bounds,
    avg_battery_capacity,
    top_10_brands,
    avg_range_by_brand,
    speed_vs_battery
)
from visualizations.charts import (
    show_avg_battery,
    show_top_brands,
    show_avg_range_by_brand,
    show_speed_vs_battery
)

# -------------------------
# Configuration page
# -------------------------
st.set_page_config(
    page_title="EV Streamlit DuckDB",
    layout="wide"
)

st.title("🚗 EV Streamlit DuckDB")

# -------------------------
# Upload CSV
# -------------------------
uploaded_file = st.file_uploader(
    "Choisissez un fichier CSV",
    type=["csv"]
)

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    store_dataframe(df)

    st.success("Données chargées et stockées dans DuckDB ✅")

    # -------------------------
    # Sidebar - Filtres
    # -------------------------
    st.sidebar.header("🎛️ Filtres")

    brands = get_brands()
    min_range, max_range = get_range_bounds()

    selected_brand = st.sidebar.selectbox(
        "Marque",
        options=["Toutes"] + brands
    )

    selected_range = st.sidebar.slider(
        "Autonomie (km)",
        min_value=min_range,
        max_value=max_range,
        value=(min_range, max_range)
    )

    brand_filter = None if selected_brand == "Toutes" else selected_brand
    min_range_filter, max_range_filter = selected_range

    # -------------------------
    # KPI - DuckDB
    # -------------------------
    avg_battery = avg_battery_capacity(
        brand=brand_filter,
        min_range=min_range_filter,
        max_range=max_range_filter
    )

    top_brands_df = top_10_brands(
        min_range=min_range_filter,
        max_range=max_range_filter
    )

    avg_range_df = avg_range_by_brand(
        brand=brand_filter,
        min_range=min_range_filter,
        max_range=max_range_filter
    )

    speed_battery_df = speed_vs_battery(
        brand=brand_filter,
        min_range=min_range_filter,
        max_range=max_range_filter
    )

    # -------------------------
    # Affichage
    # -------------------------
    st.markdown("## 📊 Indicateurs clés de performance")

    show_avg_battery(avg_battery)
    show_top_brands(top_brands_df)
    show_avg_range_by_brand(avg_range_df)
    show_speed_vs_battery(speed_battery_df)

else:
    st.info("Veuillez téléverser un fichier CSV pour afficher les indicateurs.")
