import streamlit as st
import pandas as pd
import altair as alt


def app():
    st.title("Air Quality Explorer")

    df = pd.read_csv("data/sample_air_quality.csv", parse_dates=["timestamp"])

    city = st.selectbox("City", sorted(df["city"].unique()))
    parameter = st.selectbox("Parameter", sorted(df["parameter"].unique()))

    sel = df[(df["city"] == city) & (df["parameter"] == parameter)].copy()

    if sel.empty:
        st.warning("No data for selection.")
        return

    chart = (
        alt.Chart(sel)
        .mark_line(point=True)
        .encode(x="timestamp:T", y="value:Q", tooltip=["timestamp", "value"]) 
        .properties(height=300)
    )

    st.altair_chart(chart.interactive(), use_container_width=True)

    st.subheader("Data")
    st.dataframe(sel.sort_values("timestamp", ascending=False))

    st.subheader("Map (placeholder)")
    coords = sel[["latitude", "longitude"]].dropna().rename(columns={"latitude": "lat", "longitude": "lon"})
    if not coords.empty:
        st.map(coords)
    else:
        st.write("No coordinates available for map.")
