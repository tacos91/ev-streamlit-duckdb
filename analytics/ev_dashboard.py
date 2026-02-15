import streamlit as st
import pandas as pd
import plotly.express as px
import duckdb

def run_ev_dashboard():

    st.header("🚗⚡ Tableau de Bord – Véhicules Électriques")

    fichier = st.file_uploader(
        "Importer le fichier CSV des véhicules électriques",
        type=["csv"]
    )

    if fichier is None:
        st.info("Veuillez importer le fichier CSV pour commencer l’analyse.")
        return

    # ======================
    # CHARGEMENT
    # ======================
    df = pd.read_csv(fichier)
    df.columns = df.columns.str.strip()

    # Conversion numérique sécurisée
    colonnes_numeriques = [
        "top_speed_kmh",
        "battery_capacity_kWh",
        "range_km",
        "efficiency_wh_per_km",
        "acceleration_0_100_s",
        "fast_charging_power_kw_dc",
        "torque_nm"
    ]

    for col in colonnes_numeriques:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # ======================
    # FILTRES
    # ======================
    st.sidebar.subheader("🔎 Filtres Véhicules Électriques")

    marques = sorted(df["brand"].dropna().unique())
    marques_selectionnees = st.sidebar.multiselect(
        "Sélectionner une marque",
        marques,
        default=marques
    )

    segments = sorted(df["segment"].dropna().unique())
    segments_selectionnes = st.sidebar.multiselect(
        "Segment",
        segments,
        default=segments
    )

    autonomie_min = int(df["range_km"].min())
    autonomie_max = int(df["range_km"].max())

    autonomie_selection = st.sidebar.slider(
        "Autonomie (km)",
        autonomie_min,
        autonomie_max,
        (autonomie_min, autonomie_max)
    )

    # ======================
    # APPLICATION FILTRES
    # ======================
    df_filtre = df[
        (df["brand"].isin(marques_selectionnees)) &
        (df["segment"].isin(segments_selectionnes)) &
        (df["range_km"].between(autonomie_selection[0], autonomie_selection[1]))
    ]

    if df_filtre.empty:
        st.warning("Aucun véhicule ne correspond aux filtres sélectionnés.")
        return

    # ======================
    # DUCKDB CONNECTION
    # ======================
    con = duckdb.connect(database=':memory:')
    con.register("ev_data", df_filtre)

    # ======================
    # KPI PRINCIPAUX (SQL)
    # ======================
    st.subheader("📌 Indicateurs Clés")

    query_kpi = """
    SELECT 
        COUNT(*) AS nb_vehicules,
        AVG(range_km) AS autonomie_moy,
        AVG(battery_capacity_kWh) AS batterie_moy,
        AVG(top_speed_kmh) AS vitesse_moy
    FROM ev_data
    """

    result = con.execute(query_kpi).fetchdf()

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Nombre de véhicules", int(result["nb_vehicules"][0]))
    col2.metric("Autonomie moyenne", f"{result['autonomie_moy'][0]:,.0f} km")
    col3.metric("Capacité batterie moyenne", f"{result['batterie_moy'][0]:,.1f} kWh")
    col4.metric("Vitesse moyenne", f"{result['vitesse_moy'][0]:,.0f} km/h")

    st.markdown("---")

    # ======================
    # TOP MARQUES AUTONOMIE (SQL)
    # ======================
    st.subheader("🏆 Top 10 Marques – Autonomie Moyenne")

    top_marques = con.execute("""
        SELECT brand, AVG(range_km) AS autonomie
        FROM ev_data
        GROUP BY brand
        ORDER BY autonomie DESC
        LIMIT 10
    """).fetchdf()

    fig1 = px.bar(
        top_marques,
        x="brand",
        y="autonomie",
        labels={"autonomie": "Autonomie moyenne (km)"}
    )

    st.plotly_chart(fig1, use_container_width=True)

    st.markdown("---")

    # ======================
    # CAPACITÉ VS AUTONOMIE
    # ======================
    st.subheader("📊 Capacité Batterie vs Autonomie")

    fig_corr = px.scatter(
        df_filtre,
        x="battery_capacity_kWh",
        y="range_km",
        color="segment",
        labels={
            "battery_capacity_kWh": "Capacité batterie (kWh)",
            "range_km": "Autonomie (km)"
        }
    )

    st.plotly_chart(fig_corr, use_container_width=True)

    # Corrélation calculée
    correlation = df_filtre["battery_capacity_kWh"].corr(df_filtre["range_km"])
    st.info(f"Corrélation batterie / autonomie : {correlation:.2f}")

    st.markdown("---")

    # ======================
    # HEATMAP CORRÉLATION
    # ======================
    st.subheader("📊 Matrice de Corrélation")

    corr_matrix = df_filtre[
        ["range_km", "battery_capacity_kWh", "top_speed_kmh",
         "efficiency_wh_per_km", "acceleration_0_100_s"]
    ].corr()

    fig_heatmap = px.imshow(
        corr_matrix,
        text_auto=True,
        color_continuous_scale="RdBu_r"
    )

    st.plotly_chart(fig_heatmap, use_container_width=True)

    st.markdown("---")

    # ======================
    # CONCLUSION ANALYTIQUE
    # ======================
    st.subheader("📝 Conclusion Analytique")

    st.info(f"""
    L'analyse met en évidence une corrélation de {correlation:.2f} 
    entre la capacité batterie et l’autonomie.

    Cela confirme que l’autonomie dépend fortement de la capacité énergétique,
    bien que d'autres facteurs comme l'efficacité énergétique influencent
    également la performance globale du véhicule.
    """)

    # ======================
    # DONNÉES FILTRÉES
    # ======================
    with st.expander("Afficher les données filtrées"):
        st.write(f"Nombre de lignes : {len(df_filtre)}")
        st.dataframe(df_filtre, use_container_width=True)
        st.download_button(
        label="📥 Télécharger les données filtrées (CSV)",
        data=df_filtre.to_csv(index=False),
        file_name="ev_donnees_filtrees.csv",
        mime="text/csv"
    )