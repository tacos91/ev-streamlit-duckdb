import plotly.express as px
import streamlit as st


def show_avg_battery(avg_value):
    st.metric(
        label="🔋 Capacité moyenne de batterie (kWh)",
        value=f"{avg_value:.1f}"
    )


def show_top_brands(df):
    fig = px.bar(
        df,
        x="brand",
        y="total",
        title="🏭 Top 10 marques de véhicules électriques"
    )
    st.plotly_chart(fig, width="stretch")


def show_avg_range_by_brand(df):
    fig = px.bar(
        df,
        x="brand",
        y="avg_range_km",
        title="🚘 Autonomie moyenne par marque (km)",
        labels={
            "avg_range_km": "Autonomie moyenne (km)",
            "brand": "Marque"
        }
    )
    st.plotly_chart(fig, width="stretch")


def show_speed_vs_battery(df):
    fig = px.scatter(
        df,
        x="battery_capacity_kWh",
        y="top_speed_kmh",
        title="⚡ Vitesse maximale vs capacité batterie",
        labels={
            "battery_capacity_kWh": "Capacité batterie (kWh)",
            "top_speed_kmh": "Vitesse max (km/h)"
        }
    )
    st.plotly_chart(fig, width="stretch")
