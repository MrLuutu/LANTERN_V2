import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import folium
from streamlit_folium import st_folium
from src.utils.clean_data import load_openaq


# ======================================================
# LOAD DATA
# ======================================================
def load_city_data():
    # Kampala
    ug = load_openaq("data/clean_openaq.csv")
    ug["city"] = "Kampala"
    ug["datetimelocal"] = pd.to_datetime(
        ug["datetimelocal"], format="mixed", errors="coerce"
    )

    # Boston
    bo = load_openaq("data/openaq_boston.csv")
    bo["city"] = "Boston"
    bo["datetimelocal"] = pd.to_datetime(
        bo["datetimelocal"], format="mixed", errors="coerce"
    )

    return pd.concat([ug, bo], ignore_index=True)


# ======================================================
# STREAMLIT PAGE
# ======================================================
def app():

    st.title("🌍 Air Quality Explorer")
    st.caption("Analyze PM pollution levels across Kampala and Boston")

    df = load_city_data()

    # -------------------------
    # FILTERS
    # -------------------------
    st.subheader("Filters")
    city = st.selectbox("Select City", sorted(df["city"].unique()))

    city_df = df[df["city"] == city].copy()
    if city_df.empty:
        st.warning("No data available for this city.")
        return

    parameter = st.selectbox("Select Pollutant", sorted(city_df["parameter"].unique()))
    sub = city_df[city_df["parameter"] == parameter]

    if sub.empty:
        st.warning("No data for this pollutant.")
        return

    # ======================================================
    # SUMMARY METRICS
    # ======================================================
    st.subheader("📊 Summary Metrics")

    col1, col2, col3 = st.columns(3)

    col1.metric("Highest Value", f"{sub['value'].max():.2f} {sub['unit'].iloc[0]}")
    col2.metric("Lowest Value", f"{sub['value'].min():.2f} {sub['unit'].iloc[0]}")
    col3.metric("Average Level", f"{sub['value'].mean():.2f} {sub['unit'].iloc[0]}")

    # ======================================================
    # LINE CHART
    # ======================================================
    st.subheader(f"📈 {parameter.upper()} Trend — {city}")

    line_df = (
        sub[["datetimelocal", "value"]]
        .dropna()
        .sort_values("datetimelocal")
    )

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(line_df["datetimelocal"], line_df["value"], color="steelblue", linewidth=2)

    ax.set_xlabel("Time")
    ax.set_ylabel(parameter.upper())
    ax.set_title(f"{parameter.upper()} Levels Over Time")

    plt.xticks(rotation=45)
    st.pyplot(fig)

    # ======================================================
    # FOLIUM MAP
    # ======================================================
    st.subheader("🗺️ Sensor Locations")

    coords = sub[["latitude", "longitude"]].dropna()

    if not coords.empty:
        lat_center = coords["latitude"].mean()
        lon_center = coords["longitude"].mean()

        fmap = folium.Map(location=[lat_center, lon_center], zoom_start=12)

        for _, row in coords.iterrows():
            folium.CircleMarker(
                location=[row["latitude"], row["longitude"]],
                radius=5,
                color="red",
                fill=True
            ).add_to(fmap)

        st_folium(fmap, width=750, height=500)
    else:
        st.info("No coordinate data available for this pollutant.")

    # ======================================================
    # RAW DATA + DOWNLOAD
    # ======================================================
    st.subheader("📄 Raw Data Table")

    clean_table = (
        sub[["datetimelocal", "parameter", "value", "unit", "latitude", "longitude"]]
        .sort_values("datetimelocal", ascending=False)
    )

    st.dataframe(clean_table, use_container_width=True)

    csv = clean_table.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="⬇️ Download CSV",
        data=csv,
        file_name=f"{city}_{parameter}_air_quality.csv",
        mime="text/csv",
    )
