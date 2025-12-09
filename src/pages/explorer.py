import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from src.utils.clean_data import load_openaq

#Load data for cities
def load_city_data():

    #Load for Kampala
    ug = load_openaq("data/clean_openaq.csv")
    ug["city"] = "Kampala"

    #Load for Boston
    bo = load_openaq("data/openaq_boston.csv")
    bo["city"] = "Boston"

    #Return a combined dataframe for all cities
    return pd.concat([ug, bo], ignore_index=True)

def app():
    #Set title
    st.title("Air Quality Explorer")

    #Create dataframe of the cities
    df = load_city_data()

    #Let user select city, and create subdataframe for that city only
    city = st.selectbox("City", sorted(df["city"].unique()))
    city_df = df[df["city"] == city].copy()

    #If missing data, return warning
    if city_df.empty:
        st.warning("No data for selected city.")
        return

    #Let user choose parameter (pm10, pm25) and create further subdataframe for it
    parameter = st.selectbox("Pollutant", sorted(city_df["parameter"].unique()))
    subset = city_df[city_df["parameter"] == parameter]

    #If missing data, return warning
    if subset.empty:
        st.warning("No data for selected pollutant.")
        return

    #Create line chart of chosen parameter over time
    subdf = city_df[["datetimelocal", "value"]]
    graph, axes = plt.subplots()
    axes.plot(subdf["datetimelocal"], subdf["value"])
    axes.grid(True)

    #Set labels
    axes.set_title(f"{parameter} levels over time in {city}")
    axes.set_xlabel("Date")
    axes.set_ylabel(parameter)

    #Mess around with tick spacing on x-axis
    ticks = axes.get_xticks()

    #Indexing start/stop/step
    begin_at = (len(subset) - 1) % 24 #Minus one to avoid missing final tick - most recent reading
    st.write(len(subset))
    every_24th = ticks[begin_at::24]
    axes.set_xticks(every_24th)

    #Set more readable date format for x-axis ticks

    dates = {"01": "January",
             "02": "February",
             "03": "March",
             "04": "April",
             "05": "May",
             "06": "June",
             "07": "July",
             "08": "August",
             "09": "September",
             "10": "October",
             "11": "November",
             "12": "December"}
    
    cleaned_ticks = []

    #First 4 numbers are year, then a dash, then 2 for month, dash, 2 for day
    for label in axes.get_xticklabels():
        tick = label.get_text()
        year = tick[0:4]
        month = tick[5:7]
        day = tick[8:10]
        if month in dates:
            new_tick = f"{dates[month]} {day}, {year}"

        cleaned_ticks.append(new_tick)
    
    axes.set_xticklabels(cleaned_ticks, rotation=45, ha="right")
    st.pyplot(graph)

    #Display data and map, with information relevant to user

    subset_rel = subset[["parameter", "datetimelocal", "value", "unit"]].copy()
    st.subheader("Data")
    st.dataframe(subset_rel.sort_values("datetimelocal", ascending=False))

    st.subheader("Map (placeholder)")
    coords = subset[["latitude", "longitude"]].dropna().rename(columns={"latitude": "lat", "longitude": "lon"})
    if not coords.empty:
        st.map(coords)
    else:
        st.write("No coordinates available for map.")
