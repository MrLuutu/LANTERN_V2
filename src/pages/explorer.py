import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def app():
    #Set title
    st.title("Air Quality Explorer")

    #Read data
    df = pd.read_csv("data/openaq_newtonville.csv", parse_dates=["datetimeLocal"])

    #Create boxes for city and parameter choice - need to update with cities' id's
    #Also need to change pm1 to PM10 and pm25 to PM2.5 in data cleaning
    city = st.selectbox("City", sorted(df["location_id"].unique()))
    parameter = st.selectbox("Parameter", sorted(df["parameter"].unique()))

    #Get sub data frame using city and requested parameter
    sel = df[(df["location_id"] == city) & (df["parameter"] == parameter)].copy()

    #Make sure data exists in subdataframe
    if sel.empty:
        st.warning("No data for selection.")
        return

    #Create line chart of chosen parameter over time
    subdf = sel[["datetimeLocal", "value"]]
    graph, axes = plt.subplots()
    axes.plot(subdf["datetimeLocal"], subdf["value"])

    axes.set_title(f"{parameter} levels over time in {city}")
    axes.set_xlabel("Date")
    axes.set_ylabel(parameter)

    st.pyplot(graph)
    
    #need to add bar chart of worst pollution days here or in risk?

    #Display data and map
    st.subheader("Data")
    st.dataframe(sel.sort_values("datetimeLocal", ascending=False))

    st.subheader("Map (placeholder)")
    coords = sel[["latitude", "longitude"]].dropna().rename(columns={"latitude": "lat", "longitude": "lon"})
    if not coords.empty:
        st.map(coords)
    else:
        st.write("No coordinates available for map.")
