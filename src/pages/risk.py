import streamlit as st
import pandas as pd


def compute_risk(parameter: str, value: float) -> str:
    p = (parameter or "").lower()
    try:
        v = float(value)
    except Exception:
        return "Unknown"

    if "pm25" in p or "pm2.5" in p:
        if v > 100:
            return "Very High"
        if v > 35:
            return "High"
        if v > 12:
            return "Moderate"
        return "Low"

    # Generic fallback thresholds
    if v > 200:
        return "Very High"
    if v > 100:
        return "High"
    if v > 50:
        return "Moderate"
    return "Low"


def app():
    st.title("Asthma Risk")

    df = pd.read_csv("data/sample_air_quality.csv", parse_dates=["timestamp"]) 

    city = st.selectbox("City", sorted(df["city"].unique()))
    city_df = df[df["city"] == city].copy()

    if city_df.empty:
        st.warning("No data for selected city.")
        return

    latest = city_df.sort_values("timestamp").groupby("parameter").last().reset_index()
    latest["risk"] = latest.apply(lambda r: compute_risk(r["parameter"], r["value"]), axis=1)

    st.subheader(f"Latest readings and risk for {city}")
    st.dataframe(latest[["parameter", "value", "risk"]])

    st.subheader("Risk summary")
    summary = latest["risk"].value_counts().rename_axis("risk").reset_index(name="count")
    st.table(summary)

