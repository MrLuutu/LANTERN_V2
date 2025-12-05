import streamlit as st
import pandas as pd

# Risk severity based on pm25 vs pm10 and risk thresholds
def compute_risk(parameter: str, value: float) -> str:

    #Set parameter to lowercase
    p = (parameter or "").lower()

    #Make sure value is a number
    try:
        v = float(value)
    except Exception:
        return "Unknown"

    #PM25 threshold amounts from https://www.airveda.com/blog/Understanding-Particulate-Matter-and-Its-Associated-Health-Impact
    if "pm25" in p or "pm2.5" in p:
        if v >= 250:
            return "Severe"
        elif v >= 121:
            return "Very poor"
        elif v > 91:
            return "Poor"
        elif v > 61:
            return "Moderately pollute"
        elif v > 31:
            return "Satisfactory"
        elif v < 0:
            return "Invalid Air Quality Value"
        return "Good"

    #PM10 threshold amounts from https://www.airveda.com/blog/Understanding-Particulate-Matter-and-Its-Associated-Health-Impact
    if "pm10" in p or "pm2" in p:
        if v >= 430:
            return "Severe"
        elif v >= 351:
            return "Very poor"
        elif v > 251:
            return "Poor"
        elif v > 101:
            return "Moderately pollute"
        elif v > 51:
            return "Satisfactory"
        elif v < 0:
            return "Invalid Air Quality Value"
        return "Good"

#Main running function
def app():
    #Set title
    st.title("Asthma Risk")

    #Read data into data frame
    df = pd.read_csv("data/openaq_newtonville.csv", parse_dates=["datetimeLocal"]) 

    #Do some data cleaning here

    #Mark the city - need to update so that the id matches up to a real city name
    city = st.selectbox("City", sorted(df["location_id"].unique()))
    city_df = df[df["location_id"] == city].copy()

    #Make sure city has data
    if city_df.empty:
        st.warning("No data for selected city.")
        return

    #Arrange data by time, group it by whether it's pm25 or pm10, and get the latest reading for each parameter
    latest = city_df.sort_values("datetimeLocal").groupby("parameter").last().reset_index()

    #Add risk column to the data frame based on compute_risk function
    latest["risk"] = latest.apply(lambda r: compute_risk(r["parameter"], r["value"]), axis=1)

    #Write latest readings and risk levels to the site
    st.subheader(f"Latest readings and risk for {city}")
    st.dataframe(latest[["parameter", "value", "risk"]])

    #Write summary of how many times each risk level appears, in order of highest count
    st.subheader("Risk summary")
    summary = latest["risk"].value_counts().rename_axis("risk").reset_index(name="count")
    st.table(summary)

