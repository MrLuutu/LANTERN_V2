import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from src.utils.clean_data import load_openaq

risk_levels = ["Good", "Satisfactory", "Moderately polluted", "Poor", "Very poor", "Severe"]

def compute_risk(parameter: str, value: float) -> str:
    #PM25 threshold amounts from
    #https://www.airveda.com/blog/Understanding-Particulate-Matter-and-Its-Associated-Health-Impact
    if parameter == "pm25":
        if value >= 250:
            return risk_levels[5]  # Severe
        elif value >= 121:
            return risk_levels[4]  # Very poor
        elif value >= 91:
            return risk_levels[3]  # Poor
        elif value >= 61:
            return risk_levels[2]  # Moderately polluted
        elif value >= 31:
            return risk_levels[1]  # Satisfactory
        elif value < 0:
            return "Invalid Air Quality Value"
        return risk_levels[0]  # Good

    #PM10 threshold amounts from
    #https://www.airveda.com/blog/Understanding-Particulate-Matter-and-Its-Associated-Health-Impact
    if parameter == "pm10":
        if value >= 430:
            return risk_levels[5]  # Severe
        elif value >= 351:
            return risk_levels[4]  # Very poor
        elif value >= 251:
            return risk_levels[3]  # Poor
        elif value >= 101:
            return risk_levels[2]  # Moderately polluted
        elif value >= 51:
            return risk_levels[1]  # Satisfactory
        elif value < 0:
            return "Invalid Air Quality Value"
        return risk_levels[0]  # Good

    return "Parameter not recognized"

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

#Define main function of the webpage
def app():

    #Set title
    st.title("Asthma Risk")

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

    #Get most recent available reading
    latest = subset.sort_values("timestamp").iloc[-1]

    #Show to the screen latest reading and units, to the nearst 2 decimal places
    st.subheader("Latest Reading")
    st.metric(
        label=f"{parameter.upper()} (µg/m³):",
        value=f"{latest['value']:.2f}",
    )

    #How does this reading compare to the others available?
    times_higher = latest["value"] / subset["value"].min()
    percent_of_max = (subset["value"].max() - latest["value"]) / subset["value"].max()

    st.write(f"This reading is {times_higher:.2f} times higher than the lowest reading of the past {len(subset['value'])} hours.")
    st.write(f"This reading is {percent_of_max:.0%} of the highest reading in the past {len(subset['value'])} hours.")

    #Create dictionary of colors for the risk levels
    risk_colors = {
        "Good": "green",
        "Satisfactory": "green",
        "Moderately polluted": "yellow",
        "Poor": "orange",
        "Very poor": "red",
        "Severe": "red",
    }

    #Compute risk level based on latest reading, write risk in color
    risk = compute_risk(parameter, latest["value"])
    color = risk_colors[risk]
    st.subheader(f"Current Asthma Risk Level: :{color}[{risk}]")

    #Personalization for user depending on exercise intensity
    exercise = st.slider("How intensely have you exercised today?", 0, 10, 5)
    if risk_levels.index(risk) < 4:
        if exercise >= 7:
            personal_risk = risk_levels[risk_levels.index(risk) + 2]
        elif exercise > 3:
            personal_risk = risk_levels[risk_levels.index(risk) + 1]
        else:
            personal_risk = risk
    elif risk_levels.index(risk) == 4:
        if exercise >= 3:
            personal_risk = risk_levels[5]
        else:
            personal_risk = risk
    else:
        personal_risk = risk
    personal_color = risk_colors[personal_risk]
    st.subheader(f"Your Risk Level Equivalent to: :{personal_color}[{personal_risk}]")


    #Recommendations based on risk level (asked ChatGPT for what advice to give at each level):
    recs = {
        "Good": "Normal outdoor activities can be continued. No precautions necessary.",
        "Satisfactory": "General outdoor activities are mostly safe. Sensitive individuals should monitor symptoms and keep an inhaler close by.",
        "Moderately polluted": "Limit prolonged outdoor activites. Avoid heavy exercise outdoors. Use inhaler proactively (if such use is part of your medical guidance)",
        "Poor": "Even otherwise unaffected individuals may experience respiratory symptoms. Avoid outside air. Recommended to stay indoors with an air purifier",
        "Very poor": "Most otherwise unaffected individuals will experience respiratory symptoms. Avoid all outdoor activities. Limit physical activity if air isn't filtered. Continue to monitor symptoms and follow doctor's instructions on medication/inhaler use.",
        "Severe": "Everyone is affected. Stay indoors with an air filter. Do not perform any physical activity. Have an inhaler on your person at all times. Follow your emergency asthma plan. Seek immediate medical attention if symptoms suddenly worsen or become unbearable.",
    }
    st.subheader("Recommendations")
    st.write(f"General recommendation for today: {recs[risk]}")
    st.write(f"Your recommendation for right now: {recs[personal_risk]}")

    #Show pollutant over time graph
    st.subheader(f"{parameter.upper()} levels over time in {city}")
    st.line_chart(subset.set_index("timestamp")["value"], height=400)

    risk_counts = {
        "Good": 0,
        "Satisfactory": 0,
        "Moderately polluted": 0,
        "Poor": 0,
        "Very poor": 0,
        "Severe": 0,
    }

    for index, row in subset.iterrows():
        level = compute_risk(parameter, row["value"])
        if level in risk_counts:
            risk_counts[level] += 1

    risk_counts_df = pd.DataFrame(list(risk_counts.items()), columns=["Risk Level", "Count"])
    st.dataframe(risk_counts_df)