import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import folium
from streamlit_folium import st_folium

from src.utils.clean_data import load_openaq


# ======================================================
# DATA LOADING & CLEANING
# ======================================================

def load_city_data() -> pd.DataFrame:
    """
    Load and combine Kampala and Boston air quality data.
    """
    # [DA1] Clean/manipulate data: convert timestamp strings to datetime
    ug = load_openaq("data/clean_openaq.csv")
    ug["city"] = "Kampala"
    ug["datetimelocal"] = pd.to_datetime(
        ug["datetimelocal"], format="mixed", errors="coerce"
    )

    bo = load_openaq("data/openaq_boston.csv")
    bo["city"] = "Boston"
    bo["datetimelocal"] = pd.to_datetime(
        bo["datetimelocal"], format="mixed", errors="coerce"
    )

    df = pd.concat([ug, bo], ignore_index=True)
    return df


# [PY1] Function with two or more parameters (one with default value)
# [DA4] Filter data by one condition
# [DA5] Filter data by two or more conditions with AND
def filter_data(df: pd.DataFrame, city: str, parameter: str, min_value: float = 0.0
                ) -> pd.DataFrame:
    """
    Filter by city, parameter, and a minimum value threshold.
    """
    mask = (
        (df["city"] == city) &
        (df["parameter"] == parameter) &
        (df["value"] >= min_value)
    )
    return df[mask].copy()


# [PY2] Function that returns more than one value
def compute_summary(sub: pd.DataFrame):
    """
    Compute max, min, and mean pollutant values.
    """
    max_val = sub["value"].max()
    min_val = sub["value"].min()
    mean_val = sub["value"].mean()
    unit = sub["unit"].iloc[0] if not sub.empty else ""
    return max_val, min_val, mean_val, unit


# [PY3] Error checking with try/except
# [DA6] Analyze data using a pivot-style aggregation
def try_build_pivot(sub: pd.DataFrame) -> pd.DataFrame:
    """
    Build a simple monthly average table.
    """
    try:
        temp = sub.dropna(subset=["datetimelocal"]).copy()
        temp["month"] = temp["datetimelocal"].dt.to_period("M").dt.to_timestamp()
        pivot = (
            temp.groupby("month")["value"]
            .mean()
            .reset_index()
            .rename(columns={"value": "avg_value"})
        )
        return pivot
    except Exception:
        # If anything goes wrong, return empty DataFrame
        return pd.DataFrame()


# [PY5] Dictionary using keys/values to describe pollutants
PARAMETER_LABELS = {
    "pm25": "PM2.5 (fine particulate matter)",
    "pm10": "PM10 (coarse particulate matter)",
    "no2": "NO₂ (nitrogen dioxide)",
    "o3": "O₃ (ozone)",
}


# ======================================================
# STREAMLIT PAGE
# ======================================================

def app():
    st.title("🌍 Air Quality Explorer")
    st.caption("Analyze pollution patterns for Kampala and Boston.")

    # [ST4] Customized layout & styling via description/metrics/sections
    df = load_city_data()

    # -------------------------
    # FILTERS (WIDGETS)
    # -------------------------
    st.sidebar.subheader("Filters")

    # [ST1] Widget 1: selectbox for city
    city = st.sidebar.selectbox("Select City", sorted(df["city"].unique()))

    city_df = df[df["city"] == city].copy()
    if city_df.empty:
        st.warning("No data available for this city.")
        return

    # [ST2] Widget 2: selectbox for pollutant
    parameter = st.sidebar.selectbox("Select Pollutant", sorted(city_df["parameter"].unique()))
    param_df = city_df[city_df["parameter"] == parameter].copy()
    if param_df.empty:
        st.warning("No data available for this pollutant.")
        return

    # [ST3] Widget 3: slider for minimum value threshold
    min_val_threshold = st.sidebar.slider(
        "Minimum value to include",
        float(param_df["value"].min()),
        float(param_df["value"].max()),
        float(param_df["value"].min()),
    )

    # Apply filter with minimum value
    filtered = filter_data(df, city, parameter, min_val_threshold)

    if filtered.empty:
        st.warning("No data after applying the selected filters.")
        return

    # ======================================================
    # SUMMARY METRICS
    # ======================================================
    st.subheader("📊 Summary Metrics")

    max_val, min_val, mean_val, unit = compute_summary(filtered)

    col1, col2, col3 = st.columns(3)
    col1.metric("Highest Value", f"{max_val:.2f} {unit}")
    col2.metric("Lowest Value", f"{min_val:.2f} {unit}")
    col3.metric("Average Level", f"{mean_val:.2f} {unit}")

    # Human-readable pollutant description
    # [PY4] List comprehension to format descriptive text
    desc_list = [
        f"{parameter.upper()} — {PARAMETER_LABELS.get(parameter, 'Air pollutant')}"
    ]
    st.info(" ".join(desc_list))

    # ======================================================
    # VIZ 1: LINE CHART OVER TIME
    # ======================================================
    st.subheader(f"📈 {parameter.upper()} Levels Over Time — {city}")
    # [VIZ1] Line chart with time series

    line_df = (
        filtered[["datetimelocal", "value"]]
        .dropna()
        .sort_values("datetimelocal")
    )

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(line_df["datetimelocal"], line_df["value"], linewidth=2, color="steelblue")
    ax.set_xlabel("Time")
    ax.set_ylabel(f"{parameter.upper()} ({unit})")
    ax.set_title(f"{parameter.upper()} Trend in {city}")
    plt.xticks(rotation=45)
    st.pyplot(fig)

    # ======================================================
    # VIZ 2: BAR CHART OF MONTHLY AVERAGES
    # ======================================================
    st.subheader("📊 Monthly Average Levels")
    # [DA2] Sort data; [DA3] Find top/bottom values
    pivot_df = try_build_pivot(filtered)

    if not pivot_df.empty:
        # Sort by month for consistent bar order
        pivot_df = pivot_df.sort_values("month")

        fig_bar, ax_bar = plt.subplots(figsize=(8, 3))
        ax_bar.bar(pivot_df["month"].dt.strftime("%Y-%m"), pivot_df["avg_value"], color="darkorange")
        ax_bar.set_xlabel("Month")
        ax_bar.set_ylabel(f"Avg {parameter.upper()} ({unit})")
        ax_bar.set_title(f"Average Monthly {parameter.upper()} Levels in {city}")
        plt.xticks(rotation=45)
        st.pyplot(fig_bar)
        # [VIZ2] Second visualization: bar chart
    else:
        st.info("Not enough data to compute monthly averages.")

    # Show top 5 highest pollution records table
    st.markdown("#### 🌡️ Top 5 Highest Recorded Values")
    top5 = filtered.nlargest(5, "value")  # [DA3] Find top n largest values
    st.dataframe(
        top5[["datetimelocal", "value", "unit", "latitude", "longitude"]],
        use_container_width=True,
    )

    # ======================================================
    # MAP: FOLIUM SENSOR LOCATIONS
    # ======================================================
    st.subheader("🗺️ Sensor Locations")
    # [VIZ4 MAP] Interactive map

    coords = filtered[["latitude", "longitude"]].dropna()

    if not coords.empty:
        lat_center = coords["latitude"].mean()
        lon_center = coords["longitude"].mean()

        fmap = folium.Map(location=[lat_center, lon_center], zoom_start=11)

        for _, row in coords.iterrows():
            folium.CircleMarker(
                location=[row["latitude"], row["longitude"]],
                radius=5,
                color="crimson",
                fill=True,
                fill_opacity=0.8,
            ).add_to(fmap)

        st_folium(fmap, width=750, height=500)
    else:
        st.info("No coordinates available for map display.")

    # ======================================================
    # RAW DATA TABLE + DOWNLOAD
    # ======================================================
    st.subheader("📄 Raw Data Table")

    clean_table = filtered[
        ["datetimelocal", "parameter", "value", "unit", "city", "latitude", "longitude"]
    ].sort_values("datetimelocal", ascending=False)

    st.dataframe(clean_table, use_container_width=True)

    csv = clean_table.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="⬇️ Download Filtered Data as CSV",
        data=csv,
        file_name=f"{city}_{parameter}_filtered_air_quality.csv",
        mime="text/csv",
    )

