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

    #Create subdataframe with relevant columns
    df_relevant = df[["city", "parameter", "value", "unit", "datetimelocal", "latitude", "longitude"]].copy()

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

    axes.set_title(f"{parameter} levels over time in {city}")
    axes.set_xlabel("Date")
    axes.set_ylabel(parameter)

    #Format x-axis labels to include only date and only show one ever 24 hours
   # axes.set_xticklabels([x[:10] for x in subdf["datetimelocal"]], rotation=45, ha="right")
    axes.set_xticklabels(axes.get_xticklabels(), rotation=45, ha="right")
    axes.set_xticks(axes.get_xticks()[::24])
    st.pyplot(graph)
    
    #need to add bar chart of worst pollution days here or in risk?

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
