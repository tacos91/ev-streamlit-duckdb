import streamlit as st
import pandas as pd
import plotly.express as px
import duckdb

def run_walmart_dashboard():

    st.header("🛒 Tableau de Bord – Ventes Walmart")

    fichier = st.file_uploader("Importer le fichier CSV Walmart", type=["csv"])

    if fichier is None:
        st.info("Veuillez importer le fichier CSV pour commencer l’analyse.")
        return

    # =====================
    # CHARGEMENT
    # =====================
    df = pd.read_csv(fichier)

    # =====================
    # NETTOYAGE
    # =====================
    df.columns = df.columns.str.strip()

    df["Weekly_Sales"] = (
        df["Weekly_Sales"]
        .astype(str)
        .str.replace(",", "", regex=False)
        .astype(float)
    )

    df["Date"] = pd.to_datetime(df["Date"])

    colonnes_numeriques = ["Temperature", "Fuel_Price", "CPI", "Unemployment"]
    for col in colonnes_numeriques:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # =====================
    # FILTRES
    # =====================
    st.sidebar.subheader("🔎 Filtres Walmart")

    magasins = sorted(df["Store_Number"].unique())
    magasins_selectionnes = st.sidebar.multiselect(
        "Sélectionner un magasin",
        magasins,
        default=magasins
    )

    plage_dates = st.sidebar.date_input(
        "Sélectionner la période",
        [df["Date"].min(), df["Date"].max()]
    )

    filtre_vacances = st.sidebar.selectbox(
        "Semaine spéciale",
        ["Toutes", "Uniquement vacances", "Hors vacances"]
    )

    # =====================
    # APPLICATION FILTRES
    # =====================
    df_filtre = df[df["Store_Number"].isin(magasins_selectionnes)]

    if len(plage_dates) == 2:
        df_filtre = df_filtre[
            (df_filtre["Date"] >= pd.to_datetime(plage_dates[0])) &
            (df_filtre["Date"] <= pd.to_datetime(plage_dates[1]))
        ]

    if filtre_vacances == "Uniquement vacances":
        df_filtre = df_filtre[df_filtre["Holiday_Flag"] == 1]
    elif filtre_vacances == "Hors vacances":
        df_filtre = df_filtre[df_filtre["Holiday_Flag"] == 0]

    if df_filtre.empty:
        st.warning("Aucune donnée correspondant aux filtres sélectionnés.")
        return

    # =====================
    # DUCKDB CONNECTION
    # =====================
    con = duckdb.connect(database=':memory:')
    con.register("walmart_data", df_filtre)

    # =====================
    # KPI (SQL DUCKDB)
    # =====================
    st.subheader("📌 Indicateurs Clés")

    query = """
    SELECT 
        SUM(Weekly_Sales) AS total_sales,
        AVG(Weekly_Sales) AS avg_sales,
        MAX(Weekly_Sales) AS max_sales,
        COUNT(DISTINCT Date) AS nb_weeks
    FROM walmart_data
    """

    result = con.execute(query).fetchdf()

    ventes_totales = result["total_sales"][0]
    moyenne_hebdo = result["avg_sales"][0]
    meilleure_semaine = result["max_sales"][0]
    nombre_semaines = result["nb_weeks"][0]

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Ventes Totales", f"{ventes_totales:,.0f} $")
    col2.metric("Moyenne Hebdomadaire", f"{moyenne_hebdo:,.0f} $")
    col3.metric("Meilleure Semaine", f"{meilleure_semaine:,.0f} $")
    col4.metric("Nombre de Semaines", int(nombre_semaines))

    st.markdown("---")

    # =====================
    # ÉVOLUTION TEMPORELLE
    # =====================
    st.subheader("📈 Évolution des Ventes")

    ventes_temps = con.execute("""
        SELECT Date, SUM(Weekly_Sales) as ventes
        FROM walmart_data
        GROUP BY Date
        ORDER BY Date
    """).fetchdf()

    fig1 = px.line(
        ventes_temps,
        x="Date",
        y="ventes",
        labels={"ventes": "Ventes Hebdomadaires"}
    )

    st.plotly_chart(fig1, use_container_width=True)

    st.markdown("---")

    # =====================
    # VENTES PAR MAGASIN
    # =====================
    st.subheader("🏬 Ventes par Magasin")

    ventes_magasin = con.execute("""
        SELECT Store_Number, SUM(Weekly_Sales) as ventes
        FROM walmart_data
        GROUP BY Store_Number
        ORDER BY ventes DESC
    """).fetchdf()

    fig2 = px.bar(
        ventes_magasin,
        x="Store_Number",
        y="ventes",
        labels={"ventes": "Ventes Totales"}
    )

    st.plotly_chart(fig2, use_container_width=True)

    st.markdown("---")

    # =====================
    # HEATMAP CORRÉLATION
    # =====================
    st.subheader("📊 Matrice de Corrélation")

    correlation_matrix = df_filtre[
        ["Weekly_Sales", "Temperature", "Fuel_Price", "CPI", "Unemployment"]
    ].corr()

    fig_heatmap = px.imshow(
        correlation_matrix,
        text_auto=True,
        color_continuous_scale="RdBu_r"
    )

    st.plotly_chart(fig_heatmap, use_container_width=True)

    # =====================
    # CONCLUSION ANALYTIQUE
    # =====================
    st.subheader("📝 Conclusion Analytique")

    cor_temp = correlation_matrix.loc["Weekly_Sales", "Temperature"]
    cor_fuel = correlation_matrix.loc["Weekly_Sales", "Fuel_Price"]

    conclusion = f"""
    Les ventes présentent une corrélation de {cor_temp:.2f} avec la température 
    et de {cor_fuel:.2f} avec le prix du carburant.

    Cela suggère que les facteurs économiques et climatiques ont 
    un impact mesurable sur la performance des ventes.
    """

    st.info(conclusion)

    st.markdown("---")

    # =====================
    # DONNÉES FILTRÉES
    # =====================
    with st.expander("Afficher les données filtrées"):
        st.write(f"Nombre de lignes : {len(df_filtre)}")
        st.dataframe(df_filtre, use_container_width=True)