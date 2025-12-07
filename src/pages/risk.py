import streamlit as st
import pandas as pd
from src.utils.clean_data import load_openaq


def compute_risk(parameter: str, value: float) -> str:
    # Basic static thresholds (fine for MVP)
    if parameter == "pm25":
        if value > 55:
            return "High"
        if value > 35:
            return "Moderate"
        return "Low"

    if parameter == "pm10":
        if value > 150:
            return "High"
        if value > 100:
            return "Moderate"
        return "Low"

    return "Low"


def load_city_data():
    ug = load_openaq("data/clean_openaq.csv")
    ug["city"] = "Kampala"

    bo = load_openaq("data/openaq_boston.csv")
    bo["city"] = "Boston"

    return pd.concat([ug, bo], ignore_index=True)


def app():
    st.title("Asthma Risks")

    df = load_city_data()

    city = st.selectbox("City", sorted(df["city"].unique()))
    city_df = df[df["city"] == city].copy()

    if city_df.empty:
        st.warning("No data for selected city.")
        return

    parameter = st.selectbox("Pollutant", sorted(city_df["parameter"].unique()))
    subset = city_df[city_df["parameter"] == parameter]

    if subset.empty:
        st.warning("No data for selected pollutant.")
        return

    latest = subset.sort_values("timestamp").iloc[-1]

    st.subheader("Latest Reading")
    st.metric(
        label=f"{parameter.upper()} (µg/m³)",
        value=f"{latest['value']:.2f}",
    )

    risk = compute_risk(parameter, latest["value"])
    st.subheader(f"Asthma Risk Level: {risk}")

    st.line_chart(subset.set_index("timestamp")["value"], height=400)
