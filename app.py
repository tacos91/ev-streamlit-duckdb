import streamlit as st
import pandas as pd

st.set_page_config(page_title="EV Streamlit DuckDB", layout="wide")

st.title("EV Streamlit DuckDB")
st.markdown("### Téléversement des données")

uploaded_file = st.file_uploader(
    "Choisissez un fichier CSV",
    type=["csv"]
)

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    st.success("Fichier chargé avec succès")

    st.markdown("### Aperçu des données")
    st.dataframe(df.head())

    st.markdown(f"**Nombre de lignes :** {df.shape[0]}")
    st.markdown(f"**Nombre de colonnes :** {df.shape[1]}")
else:
    st.info("Veuillez téléverser un fichier CSV pour commencer.")
