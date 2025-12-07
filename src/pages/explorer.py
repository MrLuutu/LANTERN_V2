import streamlit as st
import pandas as pd
from src.utils.clean_data import load_openaq


def load_data():
    ug = load_openaq("data/clean_openaq.csv")
    ug["city"] = "Kampala"

    bo = load_openaq("data/openaq_boston.csv")
    bo["city"] = "Boston"

    return pd.concat([ug, bo], ignore_index=True)


def app():
    st.title("Air Quality Explorer")

    df = load_data()

    city = st.selectbox("Select City", sorted(df["city"].unique()))
    parameter = st.selectbox("Pollutant", sorted(df["parameter"].unique()))

    subset = df[(df["city"] == city) & (df["parameter"] == parameter)]

    if subset.empty:
        st.warning("No data available.")
        return

    st.line_chart(
        subset.set_index("timestamp")["value"],
        height=400
    )

    st.dataframe(subset.tail(50))
